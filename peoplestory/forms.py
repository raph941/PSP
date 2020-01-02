import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from peoplestory.models import Stories, Comment


class NewStoryForm(forms.ModelForm):
    
    class Meta:
        model = Stories
        fields = ['full_name', 'story_caption', 'story', 'image']