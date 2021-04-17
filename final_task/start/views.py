import os

from django.shortcuts import render
from django.conf import settings


def index(request):
    return render(request, 'start/start.html')


def about(request):
    """

    :param request:
    :return:
    """
    data = {
        'server_version': settings.VERSION,
        'user': 'Anonymous' if request.user.is_anonymous else request.user.username,
    }

    return render(request, 'start/about.html', context=data)
