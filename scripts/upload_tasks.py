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

import requests
from tqdm import tqdm

'''读取预定义的tsv文件（按行保存需要进行识别的语音文件绝对路径），并逐个进行上传'''

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--src", default=None, help="Path of source tsv file")
parser.add_argument("-u", "--url", default=None, help="URL for upload task")

args = parser.parse_args()

def read_file():
    with open(args.src, "r+", encoding="utf-8") as src:
        lines = src.readlines()
    return lines

def upload(lines: list):
    header = {
        "Content-Type": "application/json"
    }
    for line in tqdm(lines, desc="[Uploading]"):
        data = json.dumps({
            "file_path": f"{line}"
        })

        res = requests.post(args.url, headers=header, data=data)

if __name__ == '__main__':
    paths = read_file()

    # 去除特殊符号
    paths = [path.strip() for path in paths]

    upload(paths)