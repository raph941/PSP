from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from cloudinary.models import CloudinaryField
from django.utils.text import Truncator


MALE = 'Male'
FEMALE = 'Female'
GENDER = [
    (MALE, 'male'),
    (FEMALE, 'female'),
]


class User(AbstractUser):
    is_regular = models.NullBooleanField(default=False, db_index=True)
    is_admin = models.NullBooleanField(default=False, db_index=True)


class UserProfile(models.Model):
    bio = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField( max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    nationality = models.CharField( max_length=50, null=True, blank=True)
    profile_pic = CloudinaryField('image', null=True, blank=True) 

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def truncated_bio(self):
        truncated_bio = Truncator(self.bio)
        return truncated_bio.chars(60)