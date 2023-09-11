from django import forms
from .models import NewPost, Profile
from django.forms import ModelForm


class NewPostForm(forms.ModelForm):
    post_text = forms.CharField(max_length=240, label="", widget=forms.TextInput(
        attrs={
            'placeholder': 'What is happening?!',
            'style': 'border-radius: 10px;'
        }
    ))

    class Meta:
        model = NewPost
        fields = ['post_text']
