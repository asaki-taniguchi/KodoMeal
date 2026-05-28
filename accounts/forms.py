import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={
            'placeholder': 'sample@example.com'
        })
    )
    
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'パスワード'
        })
    )
    
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={
            'placeholder': 'sample@example.com'
        })
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(   #入力欄作成
        widget=forms.TextInput(attrs={   #Input type=textにする、attrs＝そのInputにオプション追加。widget=形　attrs=オプション 
            'placeholder': 'ユーザー名'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'sample@example.com'
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
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('このメールアドレスはすでに登録されています。')
        
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if not password1:
            return password1

        errors = []

        if len(password1) < 8:
            errors.append('パスワードは8文字以上で入力してください。')

        if len(password1) > 20:
            errors.append('パスワードは20文字以内で入力してください。')

        if not re.search(r'[A-Za-z]', password1):
            errors.append('パスワードには英字を1文字以上含めてください。')

        if not re.search(r'\d', password1):
            errors.append('パスワードには数字を1文字以上含めてください。')

        if password1 in ['password', 'password123', 'test12345', 'admin1234', 'qwerty123']:
            errors.append('このパスワードは一般的すぎます。')

        if errors:
            raise forms.ValidationError(errors)

        return password1
    
    def clean(self):
        cleaned_data = super().clean()

        password1 = self.data.get('password1', '')
        password2 = self.data.get('password2', '')

        if password1 and password2 and password1 != password2:
            if not self.errors.get('password2'):
                self.add_error('password2', '確認用パスワードが一致しません。')

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]  
        if commit:
            user.save()
        return user
                                             