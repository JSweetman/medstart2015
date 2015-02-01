from django.db import models
from users.models import User

# Create your models here.
class Post(models.Model):
	# '''Medstart post model'''
	# Post statuses
	OPEN, CLOSED, DELETED = range(3)
	STATUS_CHOICES = [(OPEN, "Open"), (CLOSED, "Closed"), (DELETED, "Deleted")]

	# Post types. Answers should be listed before comments.
	QUESTION, ANSWER, COMMENT = range(3)
	TYPE_CHOICES = [
		(QUESTION, "Question"), (ANSWER, "Answer"), (COMMENT, "Comment"),
	]

	title = models.CharField(max_length=200, null=False)

	# The user that originally created the post.
	author = models.ForeignKey(User, related_name='author')

	# Indicates the information value of the post.
 #    rank = models.FloatField(default=0, blank=True)

	# post status, i.e. open, answered, or closed
	status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)

	# The type of the post: question, answer, comment.
	type = models.IntegerField(choices=TYPE_CHOICES, db_index=True)

	# Number of upvotes for the post
	vote_count = models.IntegerField(default=0, blank=True, db_index=True)

	# The number of replies that a post has.
	reply_count = models.IntegerField(default=0, blank=True)

	# The number of comments that a post has.
	comment_count = models.IntegerField(default=0, blank=True)

	# handles updated and created time fields
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	# Indicates whether the post has accepted answer.
	has_accepted = models.BooleanField(default=False, blank=True)

	# This is the HTML that the user enters.
	content = models.TextField(default='')

	# gets body of question
	@property
	def as_text(self):
		"Returns the body of the post after stripping the HTML tags"
		text = bleach.clean(self.content, tags=[], attributes=[], styles={}, strip=True)
		return text

	# short peek into post
	def peek(self, length=300):
		"A short peek at the post"
		return self.as_text[:length]

	# get title of the post
	def get_title(self):
		if self.status == Post.OPEN:
			return self.title
		else:
			return "(%s) %s" % ( self.get_status_display(), self.title)

	# check if post is open
	@property
	def is_open(self):
		return self.status == Post.OPEN

	@property
	def age_in_days(self):
		delta = const.now() - self.creation_date
		return delta.days

	@property
	def set_votecount(self):
		self.vote_count = self.vote_set.filter(vote=1).count()
		self.save()
		return self.vote_count


	def __unicode__(self):
		return self.title

SCORES = (
	(+1, '+1'),
	(-1, '-1'),
)

class Vote(models.Model):
	"""
	A vote on an object by a User.
	"""
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	vote = models.SmallIntegerField(choices=SCORES)
	time_stamp = models.DateTimeField(editable=False, auto_now=True)

	@classmethod
	def create(cls, user, post, vote):
		if post.vote_set.filter(user=user):
			return 'You have already voted on %s' % (post.title)
		else:
			print 'hello'
			new_vote = Vote(user=user, post=post, vote=vote)
			if new_vote.is_upvote():
				new_vote.post.vote_count +=1
			if new_vote.is_downvote():
				new_vote.post.vote_count -=1
			new_vote.save()
			return new_vote

	def __str__(self):
		return '%s: %s on %s' % (self.user, self.vote, self.post)

	def is_upvote(self):
		return self.vote == 1

	def is_downvote(self):
		return self.vote == -1

class Tags(models.Model):
	pass
