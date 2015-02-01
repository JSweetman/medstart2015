from django.shortcuts import render
from .models import Question, Answer
from django.shortcuts import get_object_or_404
from .forms import QuestionForm
from django.http import HttpResponseRedirect

# Create your views here.
def question_answer(request, id):
	question = get_object_or_404(Question, id=id)
	answer_set = question.answer_set.all()
	return render(request, 'posts/question.html', {'question': question, 'answer_set': answer_set})


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