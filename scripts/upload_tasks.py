# -*- coding: utf-8 -*-
'''
   Project:       offlineModelGetter
   File Name:     upload_tasks
   Author:        Chaos
   Email:         life0531@foxmail.com
   Date:          2021/5/18
   Software:      PyCharm
'''
import argparse
import json
import os

import requests
from tqdm import tqdm

'''模式①：读取预定义的tsv文件（按行保存需要进行识别的语音文件绝对路径），并逐个进行上传'''
'''模式②：给定音频文件父文件夹，自动获取当前目录下所有的文件名并进行上传，最终库内保存绝对路径，以便后期去重'''

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--src", default=None, help="Path of source tsv file")
parser.add_argument("-u", "--url", default="http://222.197.219.26:5555/getter/task/", help="URL for upload task")
parser.add_argument("-p", "--prefix", default="/dataset/speech/goodkejian/cutted/", help="Path prefix, automatic add before path")
parser.add_argument("-m", "--mode", default=2, help="weather use mode 1 or 2")
parser.add_argument("-d", "--dir", default="/dataset/speech/goodkejian/cutted", help="Directory contains wav files")
parser.add_argument("-ds", "--data-source", default=None, help="Where the audio comes from")

args = parser.parse_args()

def read_file():
    with open(args.src, "r+", encoding="utf-8") as src:
        lines = src.readlines()
    return lines

def read_dir():
    # 读取给定父文件夹，上传所有音频文件
    return [e for e in os.listdir(args.dir) if e.endswith(".wav")]

def upload(lines: list):
    header = {
        "Content-Type": "application/json"
    }
    for line in tqdm(lines, desc="[Uploading]"):
        if args.prefix:
            line = os.path.join(args.prefix, line)
        data = json.dumps({
            "file_path": f"{line}",
            "audio_source": f"{args.data_source}"
        })

        res = requests.post(args.url, headers=header, data=data)

if __name__ == '__main__':
    if args.mode == 1:
        # 使用模式①
        assert args.src, "模式①必须包含一个tsv文件路径"
        paths = read_file()

    elif args.mode == 2:
        # 使用模式②
        assert args.dir, "模式②必须包含一个音频文件夹路径"
        paths = read_dir()

    # 去除特殊符号
    paths = [path.strip() for path in paths]

    upload(paths)
