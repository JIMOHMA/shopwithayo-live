from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateMyUserForm(UserCreationForm):
  username 		= forms.CharField(label='Username', 
              widget=forms.TextInput(
                  attrs={
                    'placeholder': "Username"
                  }
                )
              )
  email 		= forms.EmailField(label='Email', 
              widget=forms.TextInput(
                  attrs={
                    'placeholder': "Your Email..."
                  }
                )
              )  
  password1 		= forms.CharField(label='Password', 
              widget=forms.PasswordInput(
                  attrs={
                    'placeholder': "Password..."
                  }
                )
              ) 
  password2 		= forms.CharField(label='Confirm Password', 
              widget=forms.PasswordInput(
                  attrs={
                    'placeholder': "Re-enter Password..."
                  }
                )
              ) 
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']