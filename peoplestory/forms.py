import datetime
from PIL import Image
from django.core.files import File

from django import forms

from peoplestory.models import Stories, Comment

class NewStoryForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    x = forms.FloatField(required=False)
    y = forms.FloatField(required=False)
    width = forms.FloatField(required=False)
    height = forms.FloatField(required=False)

    class Meta:
        model = Stories
        fields = ['full_name', 'story_caption', 'story', 'image', 'x', 'y', 'width', 'height', 'video_link']


class UpdateStoryForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    x = forms.FloatField(required=False)
    y = forms.FloatField(required=False)
    width = forms.FloatField(required=False)
    height = forms.FloatField(required=False)

    class Meta:
        model = Stories
        fields = ['full_name', 'story_caption', 'story', 'image', 'x', 'y', 'width', 'height', 'video_link']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_content']

class ContactForm(forms.Form):
    name = forms.CharField(required = True)
    from_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)