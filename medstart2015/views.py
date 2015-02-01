from django.shortcuts import render
from posts.models import Question


def index(request):
	question_set = Question.objects.all()
	return render(request, 'index.html', {'question_set': question_set})