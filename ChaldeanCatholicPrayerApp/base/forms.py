from django.forms import ModelForm
from django import forms
from .models import Room, userProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['commenters']

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=True, help_text='Fill Name')
    bio = forms.CharField(widget=forms.Textarea, max_length=4000, required=False, help_text='Tell us about yourself')
    profile_pic = forms.ImageField(required=False, help_text='Upload a profile picture')

    class Meta:
        model = User
        fields = ['name','username', 'email', 'bio','profile_pic','password1', 'password2', ]

class CustomUserUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True, help_text='Fill Name')
    bio = forms.CharField(widget=forms.Textarea, max_length=4000, required=False, help_text='Tell us about yourself')
    profile_pic = forms.ImageField(required=False, help_text='Upload a profile picture')

    class Meta:
        model = User
        fields = ['name','username', 'email', 'bio','profile_pic']