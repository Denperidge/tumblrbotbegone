from django.shortcuts import render, HttpResponse
from json import dumps
from . import funcs


# Create your views here.

def isitabot(request, blogname):
    out = funcs.is_it_a_bot(blogname)
    return HttpResponse(dumps(out))