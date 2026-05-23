from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import (
    CustomUserCreationForm,
    EmailLoginForm,
    PasswordResetRequestForm,
)
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

def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', '登録されているメールアドレスを入力してください。')
                return render(request, 'password_reset_sent.html', {'form': form})
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            reset_url = request.build_absolute_uri(
                reverse('password_reset', kwargs={
                    'uidb64': uidb64,
                    'token': token,
                })
            )
            
            print(reset_url)
            
            send_mail(
                subject='KodoMeal パスワード再設定',
                message=f'以下のURLからパスワードを再設定してください。\n{reset_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=None,
            )
            
            messages.success(request, '送信完了しました')
            
    else:
        form = PasswordResetRequestForm()
            
    return render(request, 'password_reset_sent.html', {'form': form})

def password_reset_view(request, uidb64, token):
    User = get_user_model()
    
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is None or not default_token_generator.check_token(user, token):
        return render(request, 'password_reset.html', {
            'form': None,
            'is_valid_link': False,
        })
        
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SetPasswordForm(user)
        
    form.fields['new_password1'].widget.attrs.update({
        'placeholder': '半角英数字8文字以上20文字以内'
    })
    form.fields['new_password2'].widget.attrs.update({
        'placeholder': '半角英数字8文字以上20文字以内'
    })
    
    return render(request, 'password_reset.html', {
        'form': form,
        'is_valid_link': True,
    })

def register_view(request):
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return render(request, 'register.html', {
                'form': CustomUserCreationForm(),
                'registered': True,
            })
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {
        'form': form,
        'registered': False,
        })

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
        'active_nav': 'mypage',
    })
    
@login_required
def mypage_posts_view(request):
    sort = request.GET.get('sort', 'new')
    
    posts = Post.objects.filter(
        user=request.user,
        is_draft=False
    )
    
    if sort == 'old':
        posts = posts.order_by('updated_at')
    else:
        posts = posts.order_by('-updated_at')
    
    return render(request, 'mypage_posts.html', {
        'posts': posts,
        'sort': sort,
    })
    
@login_required
def mypage_drafts_view(request):
    sort = request.GET.get('sort', 'new')
    
    drafts = Post.objects.filter(
        user=request.user,
        is_draft=True
    )
    
    if sort == 'old':
        drafts = drafts.order_by('updated_at')
    else:
        drafts = drafts.order_by('-updated_at')
    
    return render(request, 'mypage_drafts.html', {
        'drafts': drafts,
        'sort': sort,
    })

@login_required
def account_edit_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'email':
            new_email = request.POST.get('email')
            
            if not new_email:
                messages.error(request, '新しいメールアドレスを入力してください。')
                return redirect('account_edit')
            
            if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
                messages.error(request,'このメールアドレスはすでに登録されています。')
                return redirect('account_edit')
            
            request.user.email = new_email
            request.user.save()
            
            messages.success(request, 'メールアドレスを変更しました')
            return redirect('account_edit')
        
        if action == 'password':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            current_password = request.POST.get('current_password')
            
            if not password1 or not password2:
                messages.error(request, '新しいパスワードを入力してください。')
                return redirect('account_edit')
            
            if not current_password:
                messages.error(request, '現在のパスワードを入力してください。')
                return redirect('account_edit')
            
            if not request.user.check_password(current_password):
                messages.error(request, '現在のパスワードが正しくありません。')
                return redirect('account_edit')
            
            if password1 != password2:
                messages.error(request, 'パスワードが一致しません。')
                return redirect('account_edit')
            
            if len(password1) < 8 or len(password1) > 20:
                messages.error(request, 'パスワードは8文字以上20文字以下で入力してください。')
                return redirect('account_edit')
            
            request.user.set_password(password1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'パスワードを変更しました')
            return redirect('account_edit')
        
        if action == 'delete':
            user = request.user
            logout(request)
            user.delete()
            
            messages.success(request, 'アカウントを削除しました')
            return redirect('app_top')
        
    return render(request, 'account_edit.html')
    
def logout_view(request):
    logout(request)
    return redirect('app_top')


