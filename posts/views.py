from django.shortcuts import render
from .models import Question, Answer, QVote
from django.shortcuts import get_object_or_404
from .forms import QuestionForm, AnswerForm
from django.http import HttpResponseRedirect
from django.db import IntegrityError

# Create your views here.
def question_answer(request, id):
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			newAnswer = form.save(commit=False)
			newAnswer.author = request.user
			newAnswer.question = Question.objects.get(id=id)
			newAnswer.save()
			return HttpResponseRedirect('/posts/%d' %(newAnswer.question.id))
	else:
		form = AnswerForm()
		question = get_object_or_404(Question, id=id)
		answer_set = question.answer_set.all()
		return render(request, 'posts/question.html', {'question': question, 'answer_set': answer_set, 'form': form})


def ask_question(request):
	print request.user.username
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			newQuestion = form.save(commit=False)
			newQuestion.author = request.user
			newQuestion.save()
			print newQuestion.id
			return HttpResponseRedirect('/posts/%d' %(newQuestion.id))
	else:
		form=QuestionForm()
	return render(request, 'posts/ask_question.html', {'form':form})

def question_upvote(request, id):
	question = Question.objects.get(id=id)
	try:
		QVote.create(request.user, question, 1)
		return HttpResponseRedirect('/posts/%d' %(question.id))
	except IntegrityError:
		return HttpResponseRedirect('/posts/%d' %(question.id))


def question_downvote(request,id):
	question = Question.objects.get(id=id)
	try:
		QVote.create(request.user, question, -1)
		return HttpResponseRedirect('/posts/%d' %(question.id))
	except IntegrityError:
		return HttpResponseRedirect('/posts/%d' %(question.id))