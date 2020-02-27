import logging
import os
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ContentType
from aiogram import Bot, Dispatcher, executor, types
import cv2
import numpy as np
# Load the cascade
from mtcnn.mtcnn import MTCNN
# Ваш токен от BotFather
from aiogram.utils.executor import start_webhook

import model_detect

TOKEN = '689185271:AAGciGxBCtNKzOB5SvjPjuliwqxSY75GVWo'

# Логирование
logging.basicConfig(level=logging.INFO)
WEBHOOK_HOST = 'https://find-ff.herokuapp.com'
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')


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
    downloaded_file.seek(0)

    img = cv2.imdecode(np.array(bytearray(downloaded_file.read()), dtype=np.uint8), -1)
    faces = detector.detect_faces(img)
    for face in faces:
            x = face['box'][0]
            y = face['box'][1]
            w = face['box'][2]
            h = face['box'][3]
            img = img[y:y + h, x:x + w]
            cv2.imwrite(r'/tmp/temp.jpg', cv2.resize(img, (200, 200),fx=0.3,fy=0.3, interpolation=cv2.INTER_AREA))
            gender= model_detect.find('/tmp/temp.jpg', '../models/gender_model.pb', '../models/gender_label.txt')
            if gender[0]=='men':
                await bot.send_message(message.chat.id, 'Ваш пол мужской')
                count_likes= model_detect.find('/tmp/temp.jpg', '../models/likes_model_men.pb',
                                              '../models/likes_label_men.txt')

                await bot.send_message(message.chat.id, 'Ваш пол мужской'+count_likes[0])
    if len(faces)==0:
        await bot.send_message(message.chat.id, 'На фото нет лиц')




@dp.message_handler(commands='start')
async def start(message: types.Message):
    button = KeyboardButton('Инструкция')
    # Добавляем
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    # Отправляем сообщение с кнопкой
    await bot.send_message(message.chat.id, 'Приветствую {}'.format(message.chat.first_name), reply_markup=kb)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass

#--------------------Запуск бота-------------------------
if __name__ == '__main__':
    heroku_start = True

    if heroku_start:
        start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                      on_startup=on_startup, on_shutdown=on_shutdown,
                      host=WEBAPP_HOST, port=WEBAPP_PORT)
    else:
        executor.start_polling(dp, skip_updates=True)

