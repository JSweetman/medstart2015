from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(verbose_name = 'bio', max_length = 255, default='', blank=True)
    ## TODO make drop down
    school = models.CharField(verbose_name = 'school', max_length = 50, default='', blank=False)
    location = models.CharField(verbose_name = 'location', max_length = 50, default='', blank=True)
    specialty = models.CharField(verbose_name = 'specialty', max_length = 50, default='', blank=True)
    ## TODO make drop down
    academic_status = models.CharField(verbose_name = 'academic_status', max_length = 30, default='', blank=True)
    reputation = models.IntegerField(default=0, blank=True, db_index=True)


    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
