from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'ユーザー名'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'sampla@example.com'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'パスワード'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'パスワード再入力'
        })
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data["email"]  
    if commit:
        user.save()
    return user
                                             