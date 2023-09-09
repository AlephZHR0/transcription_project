import os

from pytube import YouTube


def download_youtube_audio(link: str) -> str:
    """
    Downloads a video from YouTube and returns the file name

    Args:
        link (str): full link to the YouTube video

    Returns:
        str: file name of the downloaded video
    """
    if link == ".":
        exit()
    print("Downloading youtube video")
    try:
        video = YouTube(link)
    except Exception:
        print("Invalid link\nTry again with a valid link")
    stream = video.streams.get_audio_only()
    try:
        stream.download("yt_downloads")
    except FileNotFoundError:
        os.mkdir("yt_downloads")
        stream.download("yt_downloads")
    file_name = stream.default_filename
    print("Downloaded successfully")
    return f"yt_downloads/{file_name}"
