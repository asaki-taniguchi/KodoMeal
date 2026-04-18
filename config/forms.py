from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    
    username = forms.CharField(
        label='メールアドレス',
        widget=forms.TextInput(attrs={
            'placeholder': 'sample@example.com',
            'class': 'input-field'
        })
    )
    
    username = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={
            'placeholder': '半角英数字8文字以上20文字以内',
            'class': 'input-field'
        })
    )
