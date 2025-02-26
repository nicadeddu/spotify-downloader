# Spotify Playlist Downloader

List and search each track on your Spotify playlist and download the best match from YouTube Music.

## Features
- No premium required
- No login required
- Lightweight
- Downloads in higher bitrate (around 256 kbps)
- Embed metadata

## Warning
This program uses YouTube Music as the source for music downloads, there is a chance of mismatching.

> This program is for **educational purposes only**. Users are responsible for complying with YouTube Music and Spotify's terms of service.

## Usage
```sh
python -m cli <playlist_url>
```

## Dependencies
Unlike most downloader, this program does not require a Spotify Developers account. However you should have these libraries installed: 

- [innertube](https://github.com/tombulled/innertube)
- [SpotAPI](https://github.com/Aran404/SpotAPI)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://www.ffmpeg.org/)

Alternatively, install from [requirements.txt](requirements.txt) using pip (and FFmpeg build from the official website).

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you find issues or have suggestions.

This project uses flake8 for linting. Please ensure your code passes flake8 linting before submitting a pull request.

## License
This software is licensed under the [MIT License](https://github.com/invzfnc/spotify-downloader/blob/main/LICENSE) © [Cha](https://github.com/invzfnc)
