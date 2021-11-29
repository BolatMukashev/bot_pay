from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import *

PATH_TO_SAVE = r'F:/bolat/youtube_video'
PATH_TO_SAVE_CLIP = r'F:\bolat\youtube_video\clips'


def download_video(url, quality):
    video = YouTube(url, on_progress_callback=on_progress).streams.filter(progressive=True,
                                                                          file_extension='mp4',
                                                                          res=quality).first()
    title = video.title
    video.download(PATH_TO_SAVE)
    return title


def create_clip(input_name, output_name, start: str, end: str):
    path_to_video = os.path.join(PATH_TO_SAVE, f'{input_name}.mp4')
    clip = VideoFileClip(path_to_video).subclip(start, end)
    path_to_save = os.path.join(PATH_TO_SAVE_CLIP, f'{output_name}.mp4')
    try:
        clip.write_videofile(path_to_save)
    except OSError:
        pass


if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=GMkAKMTEku4&ab_channel=varlamov'
    video_title = download_video(video_url, '720p')
    # create_clip(video_title, 'clip2', '00:17:15.0', '00:19:50.9')
