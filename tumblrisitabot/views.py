from django.shortcuts import render, HttpResponse
from json import dumps
from .bot_detector import is_it_a_bot


# Create your views here.

def isitabot(request, blogname):
    out = is_it_a_bot(blogname)
    return HttpResponse(dumps(out))