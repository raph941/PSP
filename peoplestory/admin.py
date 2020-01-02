from django.contrib import admin
from .models import Stories
from .models import Comment

# Register your models here.
admin.site.register(Stories)
admin.site.register(Comment)