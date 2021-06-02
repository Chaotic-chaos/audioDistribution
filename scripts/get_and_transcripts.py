# -*- coding: utf-8 -*-
'''
   Project:       offlineModelGetter
   File Name:     get_and_transcripts
   Author:        Chaos
   Email:         life0531@foxmail.com
   Date:          2021/5/26
   Software:      PyCharm
'''
import argparse
import tempfile
import threading
import time

import librosa
import requests
import json

'''
get a audio from server and request for transcription
    1. get an audio file from the server
    2. send the file to the @lovefan server to get a transcription
    3. request the server, update the text
'''

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", default="http://222.197.219.26:5555/", help="URL of the server")
parser.add_argument("-t", "--transcript_url", default="http://lovemefan.top:8000/asr", help="URL of the asr @lovefan")
parser.add_argument("-l", "--limit", default=None, help="Limitation of tasks")
# multi-threads is currently not available.
parser.add_argument("-th", "--threads", default=1, help="Threads count")
parser.add_argument("-m", "--max_retry_times", default=5, help="Retry times if server is 500")

args = parser.parse_args()

mutex = threading.Lock()
total_num = 0

def get_audio():
    # get an audio file from the server
    response = requests.post(url=f"{args.url}getter/audio/")

    try:
        task_id = response.headers['Content-Disposition'].split(";")[-1].split("=")[-1].split(".")[0]
    except Exception as e:
        # no more tasks
        if json.loads(response.text)['code'] == 404:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) }] [Waring] [{threading.currentThread().name}]: There's no more tasks\n")
            return

    # create a temp file object
    file = response.content

    return task_id, file

def get_transcription(audio_file):
    '''
    Get transcript, find the longest sentence from the result
    :param audio_file:
    :return:
    '''
    files = {
        'file': audio_file,
    }
    res = json.loads(requests.post(url=args.transcript_url, files=files).text)

    return res['result']

def upload_text(task_id, text):
    '''
    update the text for the task
    :param task_id:
    :param text:
    :return:
    '''
    global total_num
    data = {
        "task_id": int(task_id),
        "transcript": text,
    }
    response = requests.post(url=f"{args.url}getter/transcript/", data=json.dumps(data))
    if response.status_code == 200:
        mutex.acquire()
        total_num += 1
        mutex.release()
        print(f"##################################################\n"
              f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) }] [Logging] [{threading.currentThread().name}] Task-{task_id}: '{text}' updated.\nBy {threading.currentThread().name}\n"
              f"##################################################\n")

def run():
    global total_num
    while True:
        if args.limit is not None:
            mutex.acquire()
            # there's a limitation setted by user
            if total_num >= args.limit:
                mutex.release()
                # hit the max limitation, return the function
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) }] [Warning] [{threading.currentThread().name}]: Hit the max limitation {args.limit}, stop the function.")
                return
            mutex.release()

        try:
            task_id, audio = get_audio()
        except :
            return

        retry_counter = 0
        while retry_counter < args.max_retry_times:
            try:
                text = get_transcription(audio)
                upload_text(task_id, text)
                break
            except :
                retry_counter += 1
                continue

        if retry_counter >= args.max_retry_times:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) }] [Error] [{threading.currentThread().name}]: Task-{task_id} update failed after {args.max_retry_times} times trying.")

        # text = f"test{threading.currentThread().name}"

        # upload_text(task_id, text)



if __name__ == '__main__':
    threads = []

    for i in range(1, args.threads+1):
        threads.append(
            threading.Thread(target=run, name=f"Thread-{i}")
        )

    # multi-threads is currently not available.
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
