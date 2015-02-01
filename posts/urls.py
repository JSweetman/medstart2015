from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'medstart2015.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<id>\d+)/$', views.question_answer),
    url(r'^ask/$', views.ask_question),
    url(r'^upvote/question/(?P<id>\d+)/$', views.question_upvote),
	url(r'^downvote/question/(?P<id>\d+)/$', views.question_downvote),
	url(r'^upvote/answer/(?P<id>\d+)/$', views.answer_upvote),
	url(r'^downvote/answer/(?P<id>\d+)/$', views.answer_downvote),
)
