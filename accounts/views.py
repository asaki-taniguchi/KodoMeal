from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from posts.models import Post

def register_view(request):
    if request.method == 'POST': #フォーム送信されたかのチェック
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form':form})

@login_required
def mypage_view(request):
    posts = Post.objects.filter(
            is_draft=False
    ).order_by('-created_at')
    
    drafts = Post.objects.filter(
        is_draft=True
    ).order_by('-created_at')
    
    return render(request, 'mypage.html', {
        'posts': posts,
        'drafts': drafts,
    })

def logout_view(request):
    logout(request)
    return redirect('app_top')

