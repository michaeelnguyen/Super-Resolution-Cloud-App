from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name' , 'email', 'password1', 'password2']

class CustomerForm(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), disabled=True, label='Username')
    customer_First_Name = forms.CharField(disabled=True, label='First Name')
    customer_Last_Name = forms.CharField(disabled=True, label='Last Name')
    customer_Email = forms.CharField(label='Email')
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['is_staff', 'slug', 'is_active']
