from spotapi import Public
from innertube import InnerTube
from yt_dlp import YoutubeDL

def extract_playlist_id(url):
    if "open.spotify.com" in url:
        return url.lstrip("https://open.spotify.com/playlist/").split("?si=")[0]
    
def get_playlist_titles(playlist_id):
    """Returns list of song titles with artist names in specified playlist."""

    items = next(Public.playlist_info(playlist_id))["items"]

    songs = []
    
    for item in items:
        item = item["itemV2"]["data"]
        title = item["name"]
        artist = item["artists"]["items"][0]["profile"]["name"]
        songs.append(f"{title} - {artist}")

    return songs

def get_song_url(search_text):
    """Simulates searching from the YTMusic web and returns the url
    of first song result."""

    client = InnerTube("WEB_REMIX", "1.20250203.01.00")
    data = client.search(search_text)
    
    video_id = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0][
               "tabRenderer"]["content"]["sectionListRenderer"][
               "contents"][1]["musicShelfRenderer"]["contents"][0][
               "musicResponsiveListItemRenderer"]["overlay"][
               "musicItemThumbnailOverlayRenderer"]["content"][
               "musicPlayButtonRenderer"]["playNavigationEndpoint"][
               "watchEndpoint"]["videoId"]

    url = "https://music.youtube.com/watch?v=" + video_id

    return url

def get_song_urls(titles):
    urls = []
    for title in titles:
        urls.append(get_song_url(song))

    return urls

def download_from_urls(urls):
    options = {
        "format": "m4a/bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }]
    }
    with YoutubeDL(options) as ydl:
        error_code = ydl.download(urls)
    
    print(error_code)
