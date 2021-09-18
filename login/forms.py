from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from blog.models import *
from .models import *


class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form__input"


class modifyprofile(ModelForm):
    class Meta:
        model = profile
        fields = ['fname', 'lname', 'profileimg', 'age',
                  'profession', 'specialization', 'country', 'city', 'bio']


class createprofiles(ModelForm):
    class Meta:
        model = profile
        fields = '__all__'
