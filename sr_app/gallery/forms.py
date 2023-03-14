from mimetypes import init
from django import forms
from django.forms import ModelForm

from .models import Category, Photo

class PhotoForm(ModelForm):
    category = forms.ModelChoiceField(queryset=None, label="Category") 
    description = forms.CharField(label="Description")

    class Meta:
        model = Photo
        fields = '__all__'
        exclude = ['uuid', 'user','image', 'upload_date', 'model_chosen', 'niqe', 'brisque']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)