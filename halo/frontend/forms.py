from django import forms 
from django.forms import ModelForm
from django.contrib.auth.models import User
from models import *


class UserForm(forms.ModelForm):
	
	confirm_password = forms.CharField(required=True,widget=forms.PasswordInput())

	def clean(self):
		if self.cleaned_data['confirm_password']!=self.cleaned_data['password']:
			raise forms.ValidationError("Passwords don't match")
		if User.objects.exclude(pk=self.instance.pk).filter(username=self.cleaned_data['username']):
			raise forms.ValidationError('Username "{}" already in use'.format(self.cleaned_data['username']))		
		if User.objects.exclude(pk=self.instance.pk).filter(email=self.cleaned_data['email']):
			raise forms.ValidationError('Email "{}" already in use'.format(self.cleaned_data['email']))

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password',)
		widgets = {
			'password': forms.PasswordInput()
		}
    
class LoginForm(forms.Form):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# class UserForm(forms.Form):
# 	first_name = forms.CharField(max_length=100)
# 	last_name = forms.CharField(max_length=100)
# 	username = forms.CharField(max_length=50)
# 	email_address = forms.EmailField()
# 	can_email = forms.BooleanField(required=False, value="Can we email you with updates?")
# 	company_name = forms.CharField(max_length=150, required=False)
