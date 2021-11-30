import os
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video import fx

PATH_TO_SAVE = r'C:\Users\user\Desktop\картинки для сайта\youtube_video'
PATH_TO_SAVE_CLIP = r'C:\Users\user\Desktop\картинки для сайта\youtube_video\clips'


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
    # clip.fx.crop(clip, x1=50, y1=60, x2=460, y2=275)
    path_to_save = os.path.join(PATH_TO_SAVE_CLIP, f'{output_name}.mp4')
    try:
        clip.write_videofile(path_to_save)
    except OSError:
        pass


def concatenate_clips(*args, output_name=None):
    final_clip = concatenate_videoclips([*args])
    path_to_save = os.path.join(PATH_TO_SAVE_CLIP, f'{output_name}.mp4')
    final_clip.write_videofile(path_to_save)


if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=GMkAKMTEku4&ab_channel=varlamov'
    a_apa = 'https://youtu.be/eOb8hGB3FQQ'
    video_title = download_video(a_apa, '720p')
    # create_clip(video_title, 'clip3', '00:10:13.0', '00:12:15.0')
