from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EmailLoginForm
from posts.models import Post

def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'このメールアドレスは登録されていません。')
                return render(request, 'login.html', {'form': form})
            
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
            
            if user is not None:
                login(request, user)
                return redirect('app_top')
            else:
                form.add_error('password', 'パスワードが正しくありません。')
    else:
        form = EmailLoginForm()
            
    return render(request, 'login.html', {'form': form})

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
        user=request.user,
        is_draft=False
    ).order_by('-created_at')
    
    drafts = Post.objects.filter(
        user=request.user,
        is_draft=True
    ).order_by('-created_at')
    
    return render(request, 'mypage.html', {
        'posts': posts,
        'drafts': drafts,
    })
    
@login_required
def mypage_posts_view(request):
    posts = Post.objects.filter(
        user=request.user,
        is_draft=False
    ).order_by('-created_at')
    
    return render(request, 'mypage_posts.html', {
        'posts': posts,
    })
    
@login_required
def mypage_drafts_view(request):
    drafts = Post.objects.filter(
        user=request.user,
        is_draft=True
    ).order_by('-created_at')
    
    return render(request, 'mypage_drafts.html', {
        'drafts': drafts,
    })

@login_required
def account_edit_view(request):
    return render(request, 'account_edit.html')
    
    
def logout_view(request):
    logout(request)
    return redirect('app_top')


