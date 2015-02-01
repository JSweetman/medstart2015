from django.shortcuts import render
from .models import Question
from django.shortcuts import get_object_or_404

# Create your views here.
def question_answer(request, id):
	question = get_object_or_404(Question, id=id)
	answer_set = question.answer_set.all()
	return render(request, 'posts/question.html', {'question': question, 'answer_set': answer_set})
