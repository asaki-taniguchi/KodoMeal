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
    
@login_required
def mypage_posts_view(request):
    posts = Post.objects.filter(
        is_draft=False
    ).order_by('-created_at')
    
    return render(request, 'mypage_posts.html', {
        'posts': posts,
    })
    
@login_required
def mypage_drafts_view(request):
    drafts = Post.objects.filter(
        is_draft=True
    ).order_by('-created_at')
    
    return render(request, 'mypage_drafts.html', {
        'drafts': drafts,
    })

@login_required
def store_register_view(request):
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        hours = request.POST.get('hours')
        holiday = request.POST.get('holiday')
        parking = request.POST.get('parking')
        
        if not image or not name or not address:
            return render(request, 'store_register.html',{
                'error_message': '写真・店舗名・住所は必須です。',
            })

        return redirect('store_detail', store_id=1) #store_id=1は仮
    
    return render(request, 'store_register.html')

@login_required
def account_edit_view(request):
    return render(request, 'account_edit.html')
    
    
def logout_view(request):
    logout(request)
    return redirect('app_top')


