import datetime

from django import forms

from peoplestory.models import Stories, Comment


class NewStoryForm(forms.ModelForm):
    
    class Meta:
        model = Stories
        fields = ['full_name', 'story_caption', 'story', 'image']


class UpdateStoryForm(forms.ModelForm):
    
    class Meta:
        model = Stories
        fields = ['full_name', 'story_caption', 'story', 'image']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_content']

class ContactForm(forms.Form):
    name = forms.CharField(required = True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)