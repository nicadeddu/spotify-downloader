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
Contributions are welcome! If you'd like to contribute, please read our [CONTRIBUTING.md](CONTRIBUTING.md) guide for details on how to get started.

If you have encountered problems and wish to open an issue, please see [CONTRIBUTING.md](CONTRIBUTING.md#reporting-issuesasking-questions) for detailed instructions.

By following the guidelines, you can ensure your contributions fit with the overall direction of the project, align with the project's standards, and are easy to review.

## License
This software is licensed under the [MIT License](https://github.com/invzfnc/spotify-downloader/blob/main/LICENSE) © [Cha](https://github.com/invzfnc)
