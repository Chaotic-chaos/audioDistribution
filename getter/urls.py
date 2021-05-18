# -*- coding: utf-8 -*-
'''
   Project:       offlineModelGetter
   File Name:     urls
   Author:        Chaos
   Email:         life0531@foxmail.com
   Date:          2021/5/18
   Software:      PyCharm
'''
from django.urls import path
from . import views

urlpatterns = [
    path("audio/", views.get_audio, name="get_audio_from_server"),
    path("task/", views.upload_task, name="upload_one_task"),
    path("transcript/", views.update_text, name="update_text_for_one_audio"),
    path("data/", views.export_data, name="export_all_data"),
]