from django.db import models
from users.models import User

# Create your models here.
class Post(models.Model):
	content = models.TextField(default='')

	# handles updated and created time fields
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	author = models.ForeignKey(User, null=False, blank=False)

	# Number of upvotes for the post
	vote_count = models.IntegerField(default=0, blank=True, db_index=True)

	# The number of replies that a post has.
	reply_count = models.IntegerField(default=0, blank=True)

	# The number of comments that a post has.
	comment_count = models.IntegerField(default=0, blank=True)
	class Meta:
		abstract = True

class Question(Post):
	OPEN, CLOSED, DELETED = range(3)
	STATUS_CHOICES = [(OPEN, "Open"), (CLOSED, "Closed"), (DELETED, "Deleted")]

	title = models.CharField(max_length=200, null=False)

	status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)

	has_accepted = models.BooleanField(default=False, blank=True)

	# gets body of question
	@property
	def as_text(self):
		"Returns the body of the post after stripping the HTML tags"
		return self.content

	# short peek into post
	def peek(self, length=50):
		"A short peek at the post"
		return self.as_text[:length]

	# get title of the post
	def get_title(self):
		if self.status == Question.OPEN:
			return self.title
		else:
			return "(%s) %s" % ( self.get_status_display(), self.title)

	def inc_vote(self):
		self.vote_count+=1
		return self.save()

	def dec_vote(self):
		self.vote_count-=1
		return self.save()

	@property 
	def votes(self):
		return self.vote_count
	

	# check if post is open
	@property
	def is_open(self):
		return self.status == Question.OPEN

	@property
	def age_in_days(self):
		delta = const.now() - self.creation_date
		return delta.days


	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-vote_count', '-created']

SCORES = (
	(+1, '+1'),
	(-1, '-1'),
)

class Answer(Post):
	question = models.ForeignKey(Question)
	selected = models.BooleanField(default=False)

	def inc_vote(self):
		self.vote_count+=1
		return self.save()

	def dec_vote(self):
		self.vote_count-=1
		return self.save()

	@property 
	def votes(self):
		return self.vote_count

	def __unicode__(self):
		return self.content[:10]

	class Meta:
		ordering = ['-vote_count', '-created']

class QVote(models.Model):
	"""
	A vote on an object by a User.
	"""
	class Meta:
		unique_together= [('user', 'question')]

	user = models.ForeignKey(User)
	question = models.ForeignKey(Question, null=True)
	vote = models.SmallIntegerField(choices=SCORES)
	time_stamp = models.DateTimeField(editable=False, auto_now=True)

	@classmethod
	def create(cls, user, question, vote):
		new_vote = QVote(user=user, question=question, vote=vote)
		if new_vote.is_upvote():
			new_vote.question.inc_vote()
		if new_vote.is_downvote():
			new_vote.question.dec_vote()
		new_vote.save()
		return new_vote

	def __str__(self):
		return '%s: %s on %s' % (self.user, self.vote, self.question)

	def is_upvote(self):
		return self.vote == 1

	def is_downvote(self):
		return self.vote == -1

class AVote(models.Model):
	"""
	A vote on an object by a User.
	"""
	class Meta:
		unique_together= [('user', 'answer')]

	user = models.ForeignKey(User)
	answer = models.ForeignKey(Answer, null=True)
	vote = models.SmallIntegerField(choices=SCORES)
	time_stamp = models.DateTimeField(editable=False, auto_now=True)

	@classmethod
	def create(cls, user, answer, vote):
		new_vote = AVote(user=user, answer=answer, vote=vote)
		if new_vote.is_upvote():
			new_vote.answer.inc_vote()
		if new_vote.is_downvote():
			new_vote.answer.dec_vote()
		new_vote.save()
		return new_vote

	def __str__(self):
		return '%s: %s on %s' % (self.user, self.vote, self.answer)

	def is_upvote(self):
		return self.vote == 1

	def is_downvote(self):
		return self.vote == -1


class Tags(models.Model):
	pass
