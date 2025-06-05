from django.shortcuts import render


def index(request):
	"""
	Widok renderujący stronę z oknem do przeciągania i upuszczania.
	"""
	return render(request, 'uploader/index.html')
