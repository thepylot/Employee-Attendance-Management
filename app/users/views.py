from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages

from . import forms

def sign_up_view(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
        else:
            messages.warning(request, 'Please provide valid information.')
    else:
        form = forms.SignUpForm()

    return render(request, 'users/signup.html', {'form':form})

def sign_in_view(request):
    if request.method == 'POST':
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request,'Login Successful!')
        else:
            messages.error(request,'Email or password is not correct.')
    else:
        form = forms.SignInForm()
    return render(request, 'users/signin.html', {'form':form})



