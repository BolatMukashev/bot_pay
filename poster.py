import os
from PIL import Image, ImageFont, ImageDraw


def create_poster(image_name, school_name, promo_code) -> None:
    """
    До 22 знака - размер шрифта 160, потом уменьшается
    1025 пикселей - середина текста в постере
    Использовать только моноширинные шрифты, у них символы одинаковой ширины (не сьзжают)
    :param image_name: Название изображения
    :param school_name: Название автошколы
    :param promo_code: Промокод
    :return:
    """
    directory = os.path.join(os.getcwd(), 'static', 'images', image_name)
    directory2 = os.path.join(os.getcwd(), 'static', 'images', '2' + image_name)

    try:
        image = Image.open(directory)
    except FileNotFoundError:
        print('Файл изображения не найден')
    else:
        draw = ImageDraw.Draw(image)
        font_dir = os.path.join(os.getcwd(), 'static', 'fonts', 'Ubuntu_Mono', 'UbuntuMono-BoldItalic.ttf')

        school_name_font_size = 160 if len(school_name) <= 22 else 160 - int((len(school_name) * 1.5))
        promo_code_font_size = 160 if len(promo_code) <= 22 else 160 - int((len(promo_code) * 1.5))
        school_name_font = ImageFont.truetype(font_dir, size=school_name_font_size)
        promo_code_font = ImageFont.truetype(font_dir, size=promo_code_font_size)

        draw.text((1025, 350), "\"{}\"".format(school_name), (255, 255, 255), anchor="ms", font=school_name_font)
        draw.text((1025, 750), promo_code, (255, 255, 255), anchor="ms", font=promo_code_font)
        image.save(directory2, "PNG", optimize=True)
