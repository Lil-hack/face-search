
import asyncio
import io
import logging
import os
import threading
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaDocument, KeyboardButton, ReplyKeyboardMarkup
from urllib.request import urlopen
import json
import sqlite3
import os
from io import BytesIO

import imagehash

from PIL import Image
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ContentType
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, executor, types
from multiprocessing import Process, Manager
import json
import time
import cv2
import numpy as np
# Load the cascade
from mtcnn.mtcnn import MTCNN


# Ваш токен от BotFather
from aiogram.utils.executor import start_webhook

from gender_detector import gender_detect
from likes_detector import likes_detect

TOKEN = '689185271:AAGciGxBCtNKzOB5SvjPjuliwqxSY75GVWo'

# Логирование
logging.basicConfig(level=logging.INFO)
WEBHOOK_HOST = 'https://find-ff.herokuapp.com'
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

heroku_start=False
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
detector = MTCNN()


@dp.message_handler()
async def main_logic(message: types.Message):
    if message.text == 'admin':
        await bot.send_message(message.chat.id, 'haha')


@dp.message_handler(content_types=ContentType.PHOTO)
async def photo(message: types.Message):

    file_info = await bot.get_file(message.photo[-1].file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    # out = BytesIO(downloaded_file)
    # out.seek(0)


    downloaded_file.seek(0)
    # file_bytes = np.asarray(bytearray(downloaded_file.read()), dtype=np.uint8)
    # img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.imdecode(np.array(bytearray(downloaded_file.read()), dtype=np.uint8), -1)

    faces = detector.detect_faces(img)
    await bot.send_message(message.chat.id, str(faces))
    metka=True
    for face in faces:
        if metka==True:
            metka = False

            x = face['box'][0]
            y = face['box'][1]
            w = face['box'][2]
            h = face['box'][3]
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            img = img[y:y + h, x:x + w]
            cv2.imwrite(r'/tmp/123.jpg', cv2.resize(img, (200, 200),fx=0.3,fy=0.3, interpolation=cv2.INTER_AREA))
            time.sleep(1)
            gender_detect.find_gender('/tmp/123.jpg')
            likes_detect.find_likes('/tmp/123.jpg')
            await bot.send_message(message.chat.id, 'Я начал искать')
            # with conn.cursor() as cursor:
            #     conn.autocommit = True
            #     sql_get = "SELECT * FROM vk_photos WHERE levenshtein_less_equal(hash, '{}',5) <= 5  ORDER BY levenshtein_less_equal(hash, '{}',2) LIMIT 3;".format(str(hash),str(hash))
            #     cursor.execute(sql_get)
            #     photos = cursor.fetchall()
            #     for item in photos:
            #         await bot.send_message(message.chat.id, 'https://vk.com/id{}'.format(item[0]))
            #         await bot.send_message(message.chat.id, item[2])
                # if len(photos) == 0:
                #     await bot.send_message(message.chat.id, 'Мне не удалось найти похожих лиц')

    if len(faces)==0:
        await bot.send_message(message.chat.id, 'На фото нет лиц')
    await bot.send_message(message.chat.id, 'все')



@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'haha')

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass

def start_proc():
    try:
        pass
    except Exception as ex:
        print(ex)
#--------------------Запуск бота-------------------------
if __name__ == '__main__':

    manager = Manager()
    user_gen = manager.list()
    my_thread = threading.Thread(target=start_proc)
    my_thread.start()

    if heroku_start:
        start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                      on_startup=on_startup, on_shutdown=on_shutdown,
                      host=WEBAPP_HOST, port=WEBAPP_PORT)
    else:
        executor.start_polling(dp, skip_updates=True)

