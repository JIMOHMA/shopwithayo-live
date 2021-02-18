from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateMyUserForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from product_category.models import Customer

# Create your views here.
def loginPage(request):

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    newUser = authenticate(request, username=username, password=password)

    if newUser is not None:
      login(request, newUser)
      return redirect('home')

    else:
      messages.info(request, 'User name Or password is incorrect!')

  context = {}
  return render(request, 'accounts/login.html', context)

def logoutUser(request):
  logout(request)
  return redirect('accounts:login')

def registerPage(request):
  form = CreateMyUserForm()

  if request.method == 'POST':
    form = CreateMyUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      print("Form is valid")
      Customer.objects.create(user=user,name=user.username, email=user.email) #customer is now attached to new user

      username = request.POST.get('username')
      messages.success(request, 'Account created for {}'.format(username))

      return redirect('accounts:login')

    else: 
      print("Form is not valid")

  context = {'form': form}
  return render(request, 'accounts/register.html', context)

  # def signup(request):
  #   if request.user.is_authenticated:
  #       return redirect('home')
  #   if request.method == 'POST':
  #       form = CreateMyUserForm(request.POST)
  #       if form.is_valid():
  #           form.save()
  #           username = form.cleaned_data.get('username')
  #           password = form.cleaned_data.get('password1')
  #           user = authenticate(username=username, password=password)
  #           login(request, user)
  #           return redirect('/')
  #       else:
  #           return render(request, 'signup.html', {'form': form})
  #   else:
  #       form = UserCreationForm()
  #       return render(request, 'signup.html', {'form': form})