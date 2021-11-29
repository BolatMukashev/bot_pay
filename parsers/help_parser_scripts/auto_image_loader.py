import pyautogui as pg
from time import sleep
import os

# print(pg.position())

path = os.getcwd()

path_to_img = os.path.join(path, 'images')
all_images = [name for name in os.listdir(path_to_img)]
try:
    all_images.remove('Thumbs.db')
except:
    pass
# img_count = len(all_images)

path_to_file = os.getcwd()
file_name = 'img_id.txt'

def read_file(file_name):    
    with open(file_name, encoding='utf-8-sig', mode='r') as f:
        text = f.readlines()
        new_text = []
        for el in text:
            el = el.splitlines()
            new_text.append(el[0])
    return new_text
    
# img_id_list_count = len(lines)

menu = pg.Point(x=586, y=614)
choise_first_photo = pg.Point(x=429, y=217)
cancel_button = pg.Point(x=719, y=500)

def add_photos_to_telegram():
    print('Загрузка началась')
    while True:
        lines = read_file(file_name)
        start_id_list_count = len(lines)

        # добавление фото
        all_images = [name for name in os.listdir(path_to_img)]
        try:
            all_images.remove('Thumbs.db')
        except:
            pass
        img_count = len(all_images)
        if img_count > 0:
            pg.click(menu)
            sleep(2)
            pg.click(choise_first_photo)
            pg.typewrite(["enter"])
            sleep(1)
            pg.typewrite(["enter"])

            # удаление фото
            while True:
                lines = read_file(file_name)
                end_id_list_count = len(lines)
                if end_id_list_count != start_id_list_count:
                    pg.click(menu)
                    sleep(2)
                    pg.click(choise_first_photo)
                    pg.typewrite(["delete"])
                    pg.click(cancel_button)
                    break
                else:
                    continue
        else:
            print('Поздравляю! Загрузка фотографий в телеграм окончена!')
            break

if __name__ == "__main__":
    add_photos_to_telegram()