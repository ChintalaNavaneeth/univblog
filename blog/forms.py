from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from login.models import profile


from .models import *


class createblog(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        # exclude = ['slug', '

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs["class"] = "form__input"


CKEDITOR_SETTINGS_MODEL = {
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['ShowBlocks'],
        ['Format', 'Styles'],
        ['Bold', 'Italic', 'Underline', '-', 'Subscript',
            'Superscript', '-', 'RemoveFormat'],
    ]
}


class editblogs(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
