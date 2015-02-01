from django.shortcuts import render


def index(request):
	print 'hello'
	return render(request, 'index.html',)