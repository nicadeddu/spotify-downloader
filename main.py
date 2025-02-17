from spotapi import Public
from innertube import InnerTube
from yt_dlp import YoutubeDL

from time import sleep
from random import uniform
    
client = None

def get_playlist_info(playlist_id):
    """Extracts data from Spotify and return them in format
       `[{"title": title, "artist": artist, "length": length}]`."""

    items = next(Public.playlist_info(playlist_id))["items"]

    result = []
    
    for item in items:
        song = {}
        item = item["itemV2"]["data"]
        song["title"] = item["name"]
        song["artist"] = item["artists"]["items"][0]["profile"]["name"]
        song["length"] = int(item["trackDuration"]["totalMilliseconds"])
        result.append(song)

    return result

def convert_to_milliseconds(text):
    """Converts `"%M:%S"` timestamp from YTMusic to milliseconds."""
    minutes, seconds = text.split(":")
    return (int(minutes) * 60 + int(seconds)) * 1000
    
def get_song_url(song_info):
    """Simulates searching from the YTMusic web and returns url to closest match."""

    global client
    if client is None:
        client = InnerTube("WEB_REMIX", "1.20250203.01.00")
    data = client.search(f"{song_info['title']} {song_info['artist']}")

    top_result_length = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicCardShelfRenderer"]["subtitle"]["runs"][-1]["text"]
    first_song_length = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][1]["musicShelfRenderer"]["contents"][0]["musicResponsiveListItemRenderer"]["flexColumns"][1]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][-1]["text"]

    top_result_diff = abs(convert_to_milliseconds(top_result_length) - song_info["length"])
    first_song_diff = abs(convert_to_milliseconds(first_song_length) - song_info["length"])

    if top_result_diff < first_song_diff:
        # get top result url
        video_id = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicCardShelfRenderer"]["title"]["runs"][0]["navigationEndpoint"]["watchEndpoint"]["videoId"]
        video_title = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["musicCardShelfRenderer"]["title"]["runs"][0]["text"]
    else:
        # get first song result url
        video_id = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][1]["musicShelfRenderer"]["contents"][0]["musicResponsiveListItemRenderer"]["overlay"]["musicItemThumbnailOverlayRenderer"]["content"]["musicPlayButtonRenderer"]["playNavigationEndpoint"]["watchEndpoint"]["videoId"]
        video_title = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][1]["musicShelfRenderer"]["contents"][0]["musicResponsiveListItemRenderer"]["flexColumns"][0]["musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]

    url = "https://music.youtube.com/watch?v=" + video_id

    return url, video_title

def get_song_urls(playlist_info):
    """Repeatedly calls get_song_url on given playlist info. Returns list of results."""
    urls = []
    
    for song_info in playlist_info:
        print(f"Getting url for {song_info['title']}")
        result = get_song_url(song_info)
        urls.append(result[0])
        print(f"{result[1]} ({result[0]})")
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

    # downloads stream with highest bitrate, then save them in m4a format
    with YoutubeDL(options) as ydl:
        ydl.download(urls)
    
def main(playlist_id):
    playlist_info = get_playlist_info(playlist_id)
    download_urls = get_song_urls(playlist_info)
    download_from_urls(download_urls)
    
if __name__ == "__main__":
    main("https://open.spotify.com/playlist/2LE8ZObOZOqjsGrR6QFXwu?si=9b4a5deb005148e1") # test
