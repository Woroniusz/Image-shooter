from typing import Any

from django.http import HttpResponse
from django.shortcuts import render


def index(request: Any) -> HttpResponse:
	""" """
	return render(request, 'uploader/index.html')
