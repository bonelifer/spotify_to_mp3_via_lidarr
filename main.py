#!/usr/bin/env python3
"""
Description: This script searches for songs from a specified artist and album on Spotify,
             finds the corresponding tracks on YouTube, and downloads them as MP3 files.
             It reads configuration values from 'env.properties' file.
Inputs: None
Outputs: MP3 files downloaded from YouTube with metadata added
Usage: 
    1. Ensure 'env.properties' is correctly configured with Spotify and YouTube API keys.
    2. Run the script with optional command-line arguments:
        -a, --artist: Specify the artist name.
        -alb, --album: Specify the album name.
        -q, --quality: Specify the preferred quality for the downloaded MP3 files. 
                       Possible values are "64", "128", "192", "256", "320".
                       Default is "192".
    3. If command-line arguments are not provided, ensure to set artist_name and album_name variables within the script.
    4. Run the script using Python 3.

Example:
    1. To download songs from the album "Red Forest" by the artist "If These Trees Could Talk" with preferred quality 320:
        $ python3 main.py --artist "If These Trees Could Talk" --album "Red Forest" --quality "320"

    2. Without command-line arguments, ensure artist_name and album_name are set within the script:
        artist_name = "If These Trees Could Talk"
        album_name = "Red Forest"
        Then run the script:
        $ python3 main.py
"""

import argparse
import configparser
import os

import spotipy
import youtube_dl
import eyed3
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Download songs from specified artist and album.")
    parser.add_argument("-a", "--artist", help="Specify the artist name.")
    parser.add_argument("-alb", "--album", help="Specify the album name.")
    parser.add_argument("-q", "--quality", help="Specify the preferred quality for the downloaded MP3 files. Possible values are '64', '128', '192', '256', '320'. Default is '192'.", default="192")
    return parser.parse_args()

def add_metadata(file_path, artist, album, title):
    """
    Add metadata to the downloaded MP3 file.
    """
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.title = title
    audiofile.tag.save()

def main():
    """
    Main function to download songs from Spotify and YouTube.
    """
    args = parse_arguments()
    
    # Read configuration values from 'env.properties'
    config = configparser.ConfigParser()
    config.read('env.properties')

    SPOTIFY_CLIENT_ID = config.get("env", "SPOTIPY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = config.get("env", "SPOTIPY_CLIENT_SECRET")
    ROOT_FOLDER = config.get("env", "ROOT_PATH")

    # Initialize Spotify client
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                                                  client_secret=SPOTIFY_CLIENT_SECRET))

    if args.artist and args.album:
        artist_name = args.artist
        album_name = args.album
    else:
        # Default values if command-line arguments are not provided
        artist_name = "George Strait"
        album_name = "Troubadour"

    # Search for the specified artist on Spotify
    artist_search = spotify.search(artist_name, 3, 0, "artist")

    # Retrieve albums of the artist
    albums = spotify.artist_albums(artist_search['artists']['items'][0]['id'], album_type="album")

    # Iterate through albums to find the specified album
    for item in albums['items']:
        if item['name'] == album_name:
            # Get details of the album from Spotify
            spotify_album = spotify.album(item['id'])
            
            # Create folder for the album if it doesn't exist
            album_folder_name = f"{artist_name}/{album_name}"
            tmp_album_path = os.path.join(ROOT_FOLDER, album_folder_name)
            if not os.path.isdir(tmp_album_path):
                os.makedirs(tmp_album_path)
            
            # Iterate through tracks in the album
            for track in spotify_album['tracks']['items']:
                # Create a search string for the track
                song_search_string = track['artists'][0]['name'] + "-" + track['name']
                print(song_search_string)
                
                # Search for the track on YouTube
                results_list = YoutubeSearch(song_search_string, max_results=1).to_dict()
                if results_list:
                    best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
                    print(best_url)
                    
                    # Set output location for the downloaded MP3 file
                    output_loc = os.path.join(tmp_album_path, '%(title)s.%(ext)s')
                    
                    # Download the track from YouTube as MP3 with preferred quality
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'download_archive': 'downloaded_songs.txt',
                        'outtmpl': output_loc,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': args.quality,
                        }],
                    }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(best_url, download=False)
                        title = info_dict.get('title', None)
                        ydl.download([best_url])
                        if title:
                            mp3_file_path = os.path.join(tmp_album_path, f"{title}.mp3")
                            add_metadata(mp3_file_path, artist_name, album_name, title)
                else:
                    print("No results found for:", song_search_string)

if __name__ == "__main__":
    main()

