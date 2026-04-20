from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST': #フォーム送信されたかのチェック
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form':form})

def mypage_view(request):
    return render(request, 'mypage.html')


