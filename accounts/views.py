from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from posts.models import Post
from stores.models import Store, StoreImage

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
def store_register_view(request):
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        business_hours = request.POST.get('business_hours')
        regular_holiday = request.POST.get('regular_holiday')
        parking_comment = request.POST.get('parking_comment')
        
        if not images or not name or not address:
            return render(request, 'store_register.html',{
                'error_message': '写真・店舗名・住所は必須です。',
            })
            
        if Store.objects.filter(name=name, address=address).exists():
            return render(request, 'store_register.html', {
                'error_message': '同じ店舗名・住所の店舗はすでに登録されています。',
            })
            
        has_parking = False
        
        if parking_comment and parking_comment != 'なし':
            has_parking = True
            
        store = Store.objects.create(
            user=request.user,
            name=name,
            address=address,
            phone_number=phone_number,
            business_hours=business_hours,
            regular_holiday=regular_holiday,
            has_parking=has_parking,
            parking_comment=parking_comment,
        )
        
        for image in images:
            StoreImage.objects.create(
                store=store,
                image=image
            )
            
        return redirect('store_detail', store_id=store.id) 
    
    return render(request, 'store_register.html')

@login_required
def account_edit_view(request):
    return render(request, 'account_edit.html')
    
    
def logout_view(request):
    logout(request)
    return redirect('app_top')


