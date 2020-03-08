from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from cloudinary.models import CloudinaryField
from django.utils.text import Truncator
from directmessages.models import Message
from directmessages.middleware import RequestMiddleware
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
import datetime


MALE = 'Male'
FEMALE = 'Female'
GENDER = [
    (MALE, 'male'),
    (FEMALE, 'female'),
]


class User(AbstractUser):
    is_regular = models.NullBooleanField(default=False, db_index=True)
    is_admin = models.NullBooleanField(default=False, db_index=True)
    email = models.EmailField(max_length=254, blank=True, unique=True)


class UserProfile(models.Model):
    bio = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField( max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    nationality = models.CharField( max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True)
    profile_pic_url = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def truncated_bio(self):
        truncated_bio = Truncator(self.bio)
        return truncated_bio.chars(60)

    @property
    def unread_messages(self):
        '''to display a list of unread messages that this user recieves'''
        unread_msg = Message.objects.all().filter(recipient=self.user, read_at=None)
        return unread_msg

    @property
    def unread_messages_from_me(self):
        '''to display a list of unread messages that this user recieves'''
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        unread_msg_from_me = Message.objects.all().filter(sender=self.user, recipient=request.user, read_at=None)
        return unread_msg_from_me

    @property
    def last_msg_from_user(self):
        '''to display a truncated last message recieved from a particular'''
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        last = Message.objects.all().filter(Q(sender=self.user, recipient=request.user) | Q(sender=request.user, recipient=self.user)).last().content
        truncated_last = Truncator(last)
        return truncated_last.chars(30)

    
    def last_seen(self):
        return cache.get('seen_%s' % self.user.pk)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def all_online_users(self):
        '''returns a list of all users that are online now'''
        return cache.get('online-now')


    