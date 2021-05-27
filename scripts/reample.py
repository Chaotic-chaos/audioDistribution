# -*- coding: utf-8 -*-
'''
   Project:       offlineModelGetter
   File Name:     reample
   Author:        Chaos
   Email:         life0531@foxmail.com
   Date:          2021/5/26
   Software:      PyCharm
'''
import argparse
import os
import subprocess
import threading

import librosa
import soundfile as sf
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--src", default=None, help="source tsv file which contains audio files' path")
parser.add_argument("-t", "--target", default=None, help="target path where the output file will save into")
args = parser.parse_args()

def resample(source_file, target_file):
    # y, sr = librosa.load(source_file, sr=None)
    # y_tgt = librosa.resample(y, sr, 16000)
    # sf.write(target_file, y_tgt, 16000)
    # alter bit rate
    subprocess.call(f"sox {source_file} -c 1 -b 16 -r 16k {target_file}")

def read_and_resample(lines: list):
    for line in lines:
        line = line.strip()
        path, filename = os.path.split(line)
        print("##########################################")
        print(f"Resampling {filename}")
        resample(line, os.path.join(args.target, filename))
        print(f"Done!")
        print(f"By {threading.current_thread().name}")
        print("##########################################")



if __name__ == '__main__':
    with open(args.src, "r+", encoding="utf-8") as s:
        lines = s.readlines()

    # for line in tqdm(lines, desc="[Resampling]"):
    #     line = line.strip()
    #     path, filename = os.path.split(line)
    #     resample(line, os.path.join(args.target, filename))

    step = int(len(lines) / 3)

    thread_1 = threading.Thread(target=read_and_resample, name="Thread-1", args=(lines[:step], ))
    thread_2 = threading.Thread(target=read_and_resample, name="Thread-2", args=(lines[step:step*2], ))
    thread_3 = threading.Thread(target=read_and_resample, name="Thread-3", args=(lines[step*2:], ))

    thread_1.start()
    thread_2.start()
    thread_3.start()

    thread_1.join()
    thread_2.join()
    thread_3.join()