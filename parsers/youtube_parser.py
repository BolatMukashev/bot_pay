import sys
import os
from pytube import YouTube
# from pytube.cli import on_progress
from moviepy.editor import VideoFileClip, concatenate_videoclips


class YoutubeVideo(object):
    """
    горизонтальное видео 1280 на 720
    вертикальное видео 1080 на 1920
    9:16 = 405 на 720
    """

    def __init__(self, url):
        self.url = url
        self.PATH_TO_ORIGINAL_VIDEO = r'C:\Users\user\Desktop\картинки для сайта\youtube_video'
        self.PATH_TO_CROPPED_VIDEOS = r'C:\Users\user\Desktop\картинки для сайта\youtube_video\clips'
        self.PATH_TO_FINAL_VIDEO = r'C:\Users\user\Desktop\картинки для сайта\youtube_video\final'
        self.video_name = self.download_video()

    def download_video(self):
        yt = YouTube(self.url, on_progress_callback=self._progress_function)
        yt_video = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        title = yt_video.title
        yt_video.download(self.PATH_TO_ORIGINAL_VIDEO)
        return title.replace(':', '')

    def cut_do_vertical_and_save(self, output_name, times: list):
        """
        Обрезать видео, сделать вертикальным и сохранить
        fps default = 24
        :param output_name: название клипа при сохранении
        :param times: лист с таймингами (от, до, смещение оси x относительно центра кадра, делать вертикальным)
        Пример: ('00:18:26.0', '00:20:24.0', -200, 1)
        :return:
        """
        path_to_video = os.path.join(self.PATH_TO_ORIGINAL_VIDEO, f'{self.video_name}.mp4')
        clips = []
        for time in times:
            clip = VideoFileClip(path_to_video).subclip(time['start'], time['end'])
            if time['vertical']:
                video_width, video_height = clip.size
                clip = clip.crop(x1=(video_width - 405 + time['x_offset']) / 2, width=405)
            clips.append(clip)
        path_to_save = os.path.join(self.PATH_TO_CROPPED_VIDEOS, f'{output_name}.mp4')
        new_clip = concatenate_videoclips(clips)
        new_clip = new_clip.resize(height=1920)                    # сохранить кусочки и горизонт?
        try:
            new_clip.write_videofile(path_to_save)
        except Exception as err:
            print(str(err))
        finally:
            new_clip.close()

    def resize_video(self, input_name, height: int = 1920):
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
        path_to_save = os.path.join(self.PATH_TO_CROPPED_VIDEOS, f'resized_{input_name}.mp4')
        try:
            clip.write_videofile(path_to_save)
        except OSError:
            pass
        else:
            return path_to_save
        finally:
            clip.close()

    @staticmethod
    def get_clip(name, path):
        path_to_video = os.path.join(path, name)
        clip = VideoFileClip(path_to_video)
        return clip

    def concatenate_clips_and_save(self, output_name, ending):
        self.clear()
        clips = []
        li = os.listdir(self.PATH_TO_CROPPED_VIDEOS)
        for clip_name in li:
            clip = self.get_clip(clip_name, self.PATH_TO_CROPPED_VIDEOS)
            clips.append(clip)

        ending_video = self.get_clip(f'{ending}.mp4', self.PATH_TO_ORIGINAL_VIDEO)
        clips.append(ending_video)

        final_clip = concatenate_videoclips(clips)
        path_to_save = os.path.join(self.PATH_TO_FINAL_VIDEO, f'{output_name}.mp4')
        try:
            final_clip.write_videofile(path_to_save)
        except OSError:
            pass
        finally:
            final_clip.close()

    @staticmethod
    def _progress_function(chunk, file_handle, bytes_remaining):
        global file_size
        current = ((file_size - bytes_remaining) / file_size)
        percent = '{0:.1f}'.format(current * 100)
        progress = int(50 * current)
        status = '█' * progress + '-' * (50 - progress)
        sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
        sys.stdout.flush()

    def clear(self):
        file_name = 'Thumbs.db'
        path1 = os.path.join(self.PATH_TO_ORIGINAL_VIDEO, file_name)
        path2 = os.path.join(self.PATH_TO_CROPPED_VIDEOS, file_name)
        path3 = os.path.join(self.PATH_TO_FINAL_VIDEO, file_name)
        for el in [path1, path2, path3]:
            if os.path.isfile(el):
                os.remove(el)


example = {'start': '00:18:26.0', 'end': '00:20:24.0', 'x_offset': 0, 'vertical': True}


if __name__ == '__main__':
    video = YoutubeVideo('https://www.youtube.com/watch?v=tzdcCa56OTw&ab_channel=varlamov')
    parts_for_cuts = [
        {'start': '00:17:03.8', 'end': '00:17:43.6', 'x_offset': 0, 'vertical': True}
    ]
    # video.cut_do_vertical_and_save(output_name='cutted_clip', times=parts_for_cuts)
    video.concatenate_clips_and_save(output_name='fin_3', ending='tyan')
