from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User
from django.contrib.auth import authenticate

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Provide a valid email address.')
    name = forms.CharField(max_length=255, help_text='Required. Provide a name.')

    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2', )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        return super(SignUpForm, self).clean() 
        
class SignInForm (forms.Form):
    email = forms.EmailField(max_length=100, label='Email')
    password = forms.CharField(max_length=100, label='Password', widget = forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and len(password) < 5:
            user = authenticate(email = email, password = password)
            if not user:
                raise forms.ValidationError('Credentials is not correct!')
        return super(SignInForm, self).clean() 