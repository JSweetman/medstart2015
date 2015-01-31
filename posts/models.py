from django.db import models

# Create your models here.
class Post(models.Model):
	# '''Medstart post model'''
	pass
    # Post statuses.
    OPEN, CLOSED, DELETED = range(3)
    STATUS_CHOICES = [(OPEN, "Open"), (CLOSED, "Closed"), (DELETED, "Deleted")]

    # Post types. Answers should be listed before comments.
    QUESTION, ANSWER, COMMENT = range(3)

    TYPE_CHOICES = [
        (QUESTION, "Question"), (ANSWER, "Answer"), (COMMENT, "Comment"),
    ]

    title = models.CharField(max_length=200, null=False)

    # The user that originally created the post.
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

 #    # The user that edited the post most recently.
 #    lastedit_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='editor')

 #    # Indicates the information value of the post.
 #    rank = models.FloatField(default=0, blank=True)

 #    # Post status: open, closed, deleted.
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)

 #    # The type of the post: question, answer, comment.
    type = models.IntegerField(choices=TYPE_CHOICES, db_index=True)

    # Number of upvotes for the post
    vote_count = models.IntegerField(default=0, blank=True, db_index=True)

    # The number of views for the post.
    # view_count = models.IntegerField(default=0, blank=True)

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

 #    # This is the  HTML that gets displayed.
 #    html = models.TextField(default='')

    # The tag value is the canonical form of the post's tags
    # tag_val = models.CharField(max_length=100, default="", blank=True)

    # The tag set is built from the tag string and used only for fast filtering
    tag_set = models.ManyToManyField(Tag, blank=True, )

    def add_tags(self, text):
        text = text.strip()
        if not text:
            return
        # Sanitize the tag value
        self.tag_val = bleach.clean(text, tags=[], attributes=[], styles={}, strip=True)
        # Clear old tags
        self.tag_set.clear()
        tags = [Tag.objects.get_or_create(name=name)[0] for name in self.parse_tags()]
        self.tag_set.add(*tags)
        #self.save()

    @property
    def as_text(self):
        "Returns the body of the post after stripping the HTML tags"
        text = bleach.clean(self.content, tags=[], attributes=[], styles={}, strip=True)
        return text

    def peek(self, length=300):
        "A short peek at the post"
        return self.as_text[:length]

    def get_title(self):
        if self.status == Post.OPEN:
            return self.title
        else:
            return "(%s) %s" % ( self.get_status_display(), self.title)

    @property
    def is_open(self):
        return self.status == Post.OPEN

    @property
    def age_in_days(self):
        delta = const.now() - self.creation_date
        return delta.days

 #    def update_reply_count(self):
 #        "This can be used to set the answer count."
 #        if self.type == Post.ANSWER:
 #            reply_count = Post.objects.filter(parent=self.parent, type=Post.ANSWER, status=Post.OPEN).count()
 #            Post.objects.filter(pk=self.parent_id).update(reply_count=reply_count)

 #    def delete(self, using=None):
 #        # Collect tag names.
 #        tag_names = [t.name for t in self.tag_set.all()]

 #        # While there is a signal to do this it is much faster this way.
 #        Tag.objects.filter(name__in=tag_names).update(count=F('count') - 1)

 #        # Remove tags with zero counts.
 #        Tag.objects.filter(count=0).delete()
 #        super(Post, self).delete(using=using)


