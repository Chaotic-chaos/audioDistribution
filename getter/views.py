import csv
import json

import librosa
from django.db.models import Q
from django.http import HttpResponse, FileResponse
from django.shortcuts import render

# Create your views here.
from getter.models import Audio


def get_audio(request):
    # 获取一个尚未识别的任务文件
    try:
        audio = Audio.objects.filter(Q(transcript='') & Q(distributed=0))[0]
        # 获取成功，更改分发状态
        audio.distributed = True
        audio.save()
    except Exception as e:
        # 无更多识别任务
        print(e)
        return HttpResponse(json.dumps({
            "code": 404,
            "msg": "There's no more task."
        }))

    # 返回该文件，文件名定义为任务id，便于后期回传
    file_format = audio.audio_path.split('.')[-1]
    file = open(audio.audio_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = "application/octet-stream"
    response['Content-Disposition'] = f"attachment;filename={audio.id}.{file_format}"
    return response

def upload_task(request):
    '''
    上传任务，每次仅接收一个任务
    :param request: 接收音频文件路径，获取该音频文件的持续时间并存入数据库
    :return: 是否上传成功
    '''
    # 获取文件
    audio_file = json.loads(str(request.body, 'utf-8'))['file_path']
    audio_source = json.loads(str(request.body, 'utf-8'))['audio_source']

    # 获取音频长度（duration）
    y, sr = librosa.load(audio_file, sr=None)
    duration = librosa.get_duration(y, sr=sr)

    # 插入数据
    audio = Audio()
    audio.audio_path = audio_file
    audio.duration = duration
    audio.transcript = ''
    audio.sample_rate = sr
    audio.source = audio_source
    audio.save()

    return HttpResponse(json.dumps({
        "code": 200,
        "msg": "Successfully add a task."
    }))

def update_text(request):
    '''
    回传客户端识别好的文本信息，更新数据库，以任务id为主键
    :param request: task_id, transcript
    :return:
    '''
    # 获取前端传参
    audio_id = json.loads(str(request.body, "utf-8"))['task_id']
    audio_transcript = json.loads(str(request.body, "utf-8"))['transcript']

    try:
        # 获取对应任务
        audio = Audio.objects.get(id=audio_id)
    except:
        return HttpResponse(json.dumps({
            "code": 404,
            "msg": "Cannot find the right task, please check your task id"
        }))

    # 更新
    audio.transcript = audio_transcript
    audio.save()

    return HttpResponse(json.dumps({
        "code": 200,
        "msg": "Successfully update the task."
    }))

def export_data(request):
    # 获取全部已经识别、未导出的音频
    audios = Audio.objects.exclude(Q(transcript="") | Q(exported=1))

    # 查看是否还有未导出数据
    if len(list(audios)) == 0:
        return HttpResponse(json.dumps({
            "code": 404,
            "msg": "There's no more unexported data."
        }))

    # 解析结果
    res = []
    for audio in audios:
        res.append([audio.id, audio.audio_path, audio.duration, audio.transcript])
        audio.exported = 1
        audio.save()

    # 返回生成的csv文件
    response = HttpResponse(content_type="text/tsv")
    response['Content-Disposition'] = "attachment;filename=export.tsv"
    writer = csv.writer(response, delimiter='\t')
    # 写入标题
    writer.writerow(['TASK-ID', 'PATH', 'DURATION', 'TRANSCRIPT'])
    writer.writerows(res)

    return response