from django.shortcuts import render
from django.http import HttpResponse


def test_list(request):
    return HttpResponse('qa-dataset: test_list')
