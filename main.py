from spotapi import Public
from innertube import InnerTube
from yt_dlp import YoutubeDL

from time import sleep
from random import uniform

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
    """Repeatedly calls get_song_url on given titles. Return list of results."""
    urls = []
    for title in titles:
        urls.append(get_song_url(title))
        sleep(uniform(1, 3))

    return urls

def download_from_urls(urls):
    """Downloads list of songs with yt-dlp"""

    # options generated from https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py
    options = {'extract_flat': 'discard_in_playlist',
         "final_ext": "m4a",
         "format": "bestaudio/best",
         "fragment_retries": 10,
         'ignoreerrors': 'only_download',
         'outtmpl': {'default': '%(title)s.%(ext)s'},
         'postprocessors': [{'key': 'FFmpegExtractAudio',
                             'nopostoverwrites': False,
                             'preferredcodec': 'm4a',
                             'preferredquality': '5'},
                            {'key': 'FFmpegConcat',
                             'only_multi_video': True,
                             'when': 'playlist'}],
         'retries': 10}
    
    with YoutubeDL(options) as ydl:
        ydl.download(urls)
    
def main(playlist_id):
    titles = get_playlist_titles(playlist_id)
    download_urls = get_song_urls(titles)
    download_from_urls(download_urls)
    
if __name__ == "__main__":
    main("https://open.spotify.com/playlist/2LE8ZObOZOqjsGrR6QFXwu?si=9b4a5deb005148e1") # test
