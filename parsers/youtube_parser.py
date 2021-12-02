import sys
import os
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import VideoFileClip, concatenate_videoclips

PATH_TO_SAVE = r'C:\Users\user\Desktop\картинки для сайта\youtube_video'
PATH_TO_SAVE_CLIP = r'C:\Users\user\Desktop\картинки для сайта\youtube_video\clips'


# горизонтальное видео 1280 на 720
# вертикальное видео 1080 на 1920
# 9:16 = 405 на 720


def progress_function(chunk, file_handle, bytes_remaining):
    global file_size
    current = ((file_size - bytes_remaining) / file_size)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()


def download_video(url):
    yt = YouTube(url, on_progress_callback=progress_function)
    video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
    title = video.title
    video.download(PATH_TO_SAVE)
    return title.replace(':', '')


def cut_video(input_name, output_name, times: list, coefficient: int = 0):
    """
    Обрезать видео
    fps default = 24
    :param coefficient:
    :param input_name:
    :param output_name:
    :param times: лист с таймингами
    :return:
    """
    path_to_video = os.path.join(PATH_TO_SAVE, f'{input_name}.mp4')
    clips = []
    for time in times:
        clip = VideoFileClip(path_to_video).subclip(time[0], time[1])
        video_width, video_height = clip.size
        clip = clip.crop(x1=(video_width - 405 + coefficient) / 2, width=405)
        clips.append(clip)
    path_to_save = os.path.join(PATH_TO_SAVE_CLIP, f'{output_name}.mp4')
    new_clip = concatenate_videoclips(clips).resize(height=1920)
    try:
        new_clip.write_videofile(path_to_save)
    except Exception as err:
        print(str(err))
    else:
        return path_to_save
    finally:
        new_clip.close()


def resize_video(input_name, height: int = 1920):
    """
    Изменить размер видео
    fps default = 24
    :param input_name:
    :param height:
    :return:
    """
    clip = VideoFileClip(input_name).subclip().resize(height=height)
    video_width, video_height = clip.size
    print(f'{video_width=} {video_height=}')
    path_to_save = os.path.join(PATH_TO_SAVE_CLIP, f'resized_{input_name}.mp4')
    try:
        clip.write_videofile(path_to_save)
    except OSError:
        pass
    else:
        return path_to_save
    finally:
        clip.close()


def get_clip(name):
    path_to_video = os.path.join(PATH_TO_SAVE_CLIP, f'{name}.mp4')
    clip = VideoFileClip(path_to_video)
    return clip


def concatenate_clips(raw_video_path, ending, output_name='final'):
    clips = []
    raw_video_ = VideoFileClip(raw_video_path)
    ending_video = VideoFileClip(os.path.join(PATH_TO_SAVE, f'{ending}.mp4'))
    clips.append(raw_video_)
    clips.append(ending_video)
    final_clip = concatenate_videoclips(clips)
    path_to_save = os.path.join(PATH_TO_SAVE_CLIP, f'{output_name}.mp4')
    try:
        final_clip.write_videofile(path_to_save)
    except OSError:
        pass
    finally:
        final_clip.close()


if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=tzdcCa56OTw&ab_channel=varlamov'
    original_video_name = download_video(video_url)
    parts_for_cuts = [
        ('00:00:00.0', '00:00:32.0'),
        ('00:01:01.5', '00:01:13.3')
    ]
    raw_video = cut_video(original_video_name, '1minute_clip', parts_for_cuts, coefficient=100)
    print(f'{raw_video=}')
    # raw_video = resize_video(raw_video)
    # print(f'{raw_video=}')
    concatenate_clips(raw_video, ending='lady', output_name='smertnost')
