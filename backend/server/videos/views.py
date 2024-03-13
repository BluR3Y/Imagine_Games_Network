from django.shortcuts import render
from django.http import HttpResponse

def tester(self):
    return HttpResponse('Hello World')