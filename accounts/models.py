from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


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
    sex = models.CharField(max_length=50, choices=GENDER, default=MALE)
    nationality = models.CharField( max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField( upload_to='profile_pics', default='face.png')

    def __str__(self):
        return f'{self.user.username} Profile'