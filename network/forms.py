from django import forms
from .models import Post, Profile
from django.forms import ModelForm


class NewPostForm(forms.ModelForm):
    post_text = forms.CharField(max_length=240, label="", widget=forms.TextInput(
        attrs={
            'placeholder': 'What is happening?!',
            'style': 'border-radius: 10px; width: 300px;'

        }
    ))

    class Meta:
        model = Post
        fields = ['post_text']
