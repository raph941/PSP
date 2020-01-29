import datetime
from PIL import Image
from django.core.files import File

from django import forms

from peoplestory.models import Stories, Comment


class NewStoryForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Stories
        fields = ['full_name', 'story_caption', 'story', 'image', 'x', 'y', 'width', 'height']
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        import pdb; pdb.set_trace()
        story = super(NewStoryForm, self).save(commit=False)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        story_image = Image.open(story.image)
        cropped_image = story_image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(story.image.path)
        
        return story


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
    message = forms.CharField(widget=forms.Textarea, required=True)