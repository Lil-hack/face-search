
import os
import sys
import threading
import uuid

import aiohttp
import asyncio
import io
import requests
# import psycopg2
from aiohttp import ClientSession
import imagehash
from PIL import Image
import random
import json
import time
import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN
from flask import Flask
import multiprocessing
# from psycopg2 import sql



# conn = psycopg2.connect(dbname='mydb', user='myuser',
#                             password='12345678', host='mydb.clryr6riinwd.eu-west-3.rds.amazonaws.com')
COUNTER = 1
list_token=[]
METKA=False
list_data=[]
list_hash=[]
CLUSTER_URL='https://main-cluster.herokuapp.com/'

with open('vk_generate/tokens.txt', 'r') as f:
    for line in f:
        list_token.append(str(line).rstrip('\n'))

app = Flask(__name__)

def crop_face(img,detector):
    try:
        faces = detector.detect_faces(img)
        print (faces)
        print('')
        for face in faces:
            #img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #roi_gray = gray[y:y+h, x:x+w]
            x=face['box'][0]
            y=face['box'][1]
            w=face['box'][2]
            h=face['box'][3]
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            img = img[y:y + h, x:x + w]
            return cv2.resize(img, (200, 200),fx=0.3,fy=0.3, interpolation=cv2.INTER_AREA)
    except:
        pass

def start_proc():
    try:
        process = multiprocessing.Process(target=run_start())
        process.start()
    except Exception as ex:
        print(ex)

@app.route('/')
def homepage():
    return "hello"

@app.route('/run')
def run():

    my_thread = threading.Thread(target=start_proc)
    my_thread.start()
    # start_proc()
    return "ok"

async def bound_fetch_zero(sem,id,session):
    # Getter function with semaphore.
        async with sem:
            await fetch_zero(id,session)


async def fetch_zero(id, session):
    url = build_url(id)
    try:
        async with session.get(url) as response:
                resp=await response.text()
                js=json.loads(resp)
                list_photo=[x for x in js['response'] if x != False]
                global list_data

                for it in list_photo:
                    for photo in it['items']:
                        if photo['likes']['count']>5000:
                            list_data.append((photo['owner_id'], photo['sizes'][-1]['url']))

    except Exception as ex:
            print(ex)

async def fetch(url,id, session,detector):
    async with session.get(url) as response:

        try:
            folder='5k_likes'
            resp=await response.read()

            img = cv2.imdecode(np.array(bytearray(resp), dtype=np.uint8), -1)
            face=crop_face(img, detector)
            cv2.imwrite(r'{}/{}.jpg'.format(folder, uuid.uuid1()), face)

            del resp
        except Exception as ex:
            print(ex)

def build_url(id):
    # url = 'https://api.vk.com/method/users.get?user_ids=id{}&access_token={}&v=5.101'.format(id,list_token[random.randrange(1,400)])

    api = 'API.photos.get({{\'owner_id\':{},\'album_id\':\'profile\',\'extended\':1,\'count\':\'10\'}})'.format(id * 25 + 1)
    for i in range(2,26):
        api+=',API.photos.get({{\'owner_id\':{},\'album_id\':\'profile\',\'extended\':1,\'count\':\'10\'}})'.format(id*25+i)
    url='https://api.vk.com/method/execute?access_token={}&v=5.101&code=return%20[{}];'.format(list_token[random.randrange(1, 400)],api)
    return url

async def bound_fetch(sem,url,id, session,detector):
    async with sem:
        await fetch(url,id, session,detector)

async def run_zero(id):
    tasks = []
    sem = asyncio.Semaphore(1000)

    async with ClientSession() as session:

        for id in range((id - 1) * 10, id * 10):
            #pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch_zero(sem,id, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        # print(responses)
        await responses
        del responses
        await session.close()

async def run(detector):

    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    connector = aiohttp.TCPConnector(limit=30)
    global list_data
    async with ClientSession(connector=connector) as session:
        # start=id*(int(len(list_data)/3))-int(len(list_data)/3)
        # print(start)
        # stop=id*(int(len(list_data)/3))
        # print(stop)

        for index in range(0,len(list_data)):
            id=list_data[index][0]
            url=list_data[index][1]
            #pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem,url,id, session,detector))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        # print(responses)
        await responses
        await session.close()
        del responses
    del detector





def run_start():
    # time.sleep(5)
    t0 = time.time()
    r=requests.get(CLUSTER_URL+'get_id')
    id= r.json()['id']
    print('id={}'.format(id))
    detector = MTCNN()
    for id in range(1,500):
        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(run_zero(id))
        loop.run_until_complete(future)
        run_time = (time.time() - t0)
        print("this took: {} minutes".format(run_time))
        print(len(list_data))

        t0 = time.time()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(run(detector))
        loop.run_until_complete(future)
        run_time = (time.time() - t0)
        print(len(list_hash))
        print("this took: {} minutes".format(run_time))
        # with conn.cursor() as cursor:
        #     conn.autocommit = True
        #     insert = sql.SQL('INSERT INTO vk_photos (user_id,hash, url) VALUES {}').format(
        #         sql.SQL(',').join(map(sql.Literal, list_hash))
        #     )
        #     cursor.execute(insert)
        #     requests.get(CLUSTER_URL+'close_id/{}'.format(id))

        list_data.clear()
        list_hash.clear()
        print(len(list_data))
    # process = multiprocessing.Process(target=run_start())
    # process.start()
    sys.exit()




if __name__ == '__main__':
    app.run()
