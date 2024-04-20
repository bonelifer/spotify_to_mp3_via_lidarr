## Spotify to MP3 Downloader

This script searches for songs from a specified artist and album on Spotify, finds the corresponding tracks on YouTube, and downloads them as MP3 files with metadata tags.

## **Requirements:**

* Python 3
* spotipy library ([https://spotipy.readthedocs.io/](https://spotipy.readthedocs.io/))
* youtube-dl library ([https://github.com/ytdl-org/youtube-dl](https://github.com/ytdl-org/youtube-dl))
* eyed3 library ([https://eyed3.readthedocs.io/en/latest/](https://eyed3.readthedocs.io/en/latest/))

## **Configuration:**

1. Create a file named `env.properties` in the same directory as this script.
2. Add the following lines to `env.properties`, replacing the placeholders with your actual Spotify Client ID, Client Secret, and desired root folder path for downloaded MP3s:
```
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
ROOT_PATH=path/to/your/download/folder
```

## **Usage:**

1. Ensure `env.properties` is configured correctly.
2. Run the script with optional command-line arguments:

   * `-a`, `--artist`: Specify the artist name.
   * `-alb`, `--album`: Specify the album name.
   * `-q`, `--quality`: Specify the preferred quality for downloaded MP3s (64, 128, 192, 256, 320). Defaults to 192.

3. If no command-line arguments are provided, ensure `artist_name` and `album_name` variables within the script are set to the desired artist and album.
4. Run the script using Python 3:

```
python3 main.py
```

## **Example:**

To download songs from the album "Red Forest" by the artist "If These Trees Could Talk" with preferred quality 320:
```
    python3 main.py --artist "If These Trees Could Talk" --album "Red Forest" --quality "320"
```

Without command-line arguments, if artist_name and album_name are set within the script to "If These Trees Could Talk" and "Red Forest" with default quality of 192, respectively:
```
    python3 main.py
```

### Note
Obtaining Spotify Client ID and Client Secret requires a Spotify developer account (https://developer.spotify.com/)

This script provides a basic functionality to download and add metadata to MP3 files. You might consider error handling and more advanced features in further development.
