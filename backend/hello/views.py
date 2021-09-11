"""
@Author: Guangzheng Hu
Student ID: 692277

Description: Test file
"""
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render

print('http://127.0.0.1:8000/hello/hgz')
def home(request,a=1,b=2,c=3):
    return HttpResponse("a:%d,b:%d,c:%d"%(a,b,c))

def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )