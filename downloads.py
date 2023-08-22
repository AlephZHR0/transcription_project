from pytube import YouTube


def from_youtube(link):
    print("Downloading youtube video")
    video = YouTube(link)
    stream = video.streams.get_audio_only()
    stream.download()
    file_name = stream.default_filename
    print("Downloaded successfully")
    return file_name