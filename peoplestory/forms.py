import datetime
from PIL import Image
from django.core.files import File

from django import forms

from peoplestory.models import Stories, Comment
from cloudinary.forms import CloudinaryFileField


class NewStoryForm(forms.ModelForm):
    x = forms.FloatField()
    y = forms.FloatField()
    width = forms.FloatField()
    height = forms.FloatField()

    class Meta:
        model = Stories
        fields = ['full_name', 'story_caption', 'story', 'image', 'x', 'y', 'width', 'height']
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }


class UpdateStoryForm(forms.ModelForm):
    x = forms.FloatField()
    y = forms.FloatField()
    width = forms.FloatField()
    height = forms.FloatField()

    class Meta:
        model = Stories
        fields = ['full_name', 'story_caption', 'story', 'image', 'x', 'y', 'width', 'height']
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_content']

class ContactForm(forms.Form):
    name = forms.CharField(required = True)
    from_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)