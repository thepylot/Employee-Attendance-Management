from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from . import forms

def sign_up_view(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            login(request, authenticate(email=email, password=password))
            return redirect('base:leaves')
        else:
            pass
    else:
        form = forms.SignUpForm()

    return render(request, 'users/signup.html', {'form':form})

def sign_in_view(request):
    if request.method == 'POST':
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                login(request, authenticate(email=email, password=password))
                return redirect('base:leaves')
            except AttributeError:
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request,'Please provide valid information.')
    else:
        form = forms.SignInForm()
    return render(request, 'users/signin.html', {'form':form})



def sign_out_view(request):
    logout(request)
    return redirect('auth:signin')   
