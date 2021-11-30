import os
from pytube import YouTube
from pytube.cli import on_progress
from moviepy.editor import VideoFileClip, concatenate_videoclips


PATH_TO_SAVE = r'C:\Users\user\Desktop\картинки для сайта\youtube_video'
PATH_TO_SAVE_CLIP = r'C:\Users\user\Desktop\картинки для сайта\youtube_video\clips'


# горизонтальное видео 1280 на 720
# вертикальное видео 1080 на 1920
# 9:16 = 405 на 720


def download_video(url, quality):
    video = YouTube(url, on_progress_callback=on_progress).streams.filter(progressive=True,
                                                                          file_extension='mp4',
                                                                          res=quality).first()
    title = video.title
    video.download(PATH_TO_SAVE)
    return title


def cut_video(input_name, output_name, times: list):
    """
    Обрезать видео
    fps default = 24
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
        clip = clip.crop(x1=(video_width-405)/2, width=405)
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
    path_to_save = os.path.join(PATH_TO_SAVE_CLIP, f'final_{output_name}.mp4')
    try:
        final_clip.write_videofile(path_to_save)
    except OSError:
        pass
    finally:
        final_clip.close()


if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=GMkAKMTEku4&ab_channel=varlamov'
    original_video_name = download_video(video_url, '720p')
    parts_for_cuts = [
        ('00:01:47.0', '00:02:26.0'),
        ('00:03:26.0', '00:03:33.0')
    ]
    raw_video = cut_video(original_video_name, '1minute_clip', parts_for_cuts)
    print(f'{raw_video=}')
    # raw_video = resize_video(raw_video)
    # print(f'{raw_video=}')
    concatenate_clips(raw_video, ending='tyan')
