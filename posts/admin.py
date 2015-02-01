from django.contrib import admin
from .models import Question, Answer, AVote, QVote
# Register your models here.

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(AVote)
admin.site.register(QVote)