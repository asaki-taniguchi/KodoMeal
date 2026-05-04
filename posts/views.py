from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post
from stores.models import Store

@login_required
def post_create(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id,
        is_closed=False
    )
    
    if request.method == 'POST':
        menu_name = request.POST.get('menu_name')
        target_age = request.POST.get('target_age')
        quantity = request.POST.get('quantity')
        quantity = int(quantity) if quantity else None
        facilities = request.POST.getlist('facility')
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        save_type = request.POST.get('save_type')
        
        is_draft = True if save_type == 'draft' else False
        
        Post.objects.create(
            user=request.user,
            store_id=store_id,
            menu_name=menu_name,
            target_age=target_age,
            quantity=quantity,
            facilities=facilities,
            content=content,
            rating=rating,
            is_draft=is_draft
        )
        
        return redirect('store_detail', store_id=store.id)
    
    return render(request, 'post_create.html', {
        'store': store
    })

def post_list(request, store_id):
    stores = [
        {'id': 1, 'name': 'キッズカフェ ひまわり'},
        {'id': 2, 'name': 'うどん屋 マルちゃん'},
        {'id': 3, 'name': 'ファミリーレストラン さくら'},
        {'id': 4, 'name': 'cafe sora'},
        {'id': 5, 'name': 'おやこダイニング nico'},
        {'id': 6, 'name': '中華ダイニング 好好'},  
    ]
    
    posts = Post.objects.filter(
        store_id=store_id,
        is_draft=False
        ).order_by('-created_at')
    
    store = next((store for store in stores if store['id'] == store_id), None)
    
    return render(request, 'post_list.html', {
        'store': store,
        'posts': posts
    })
    
def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    
    if request.method == 'POST':
        menu_name = request.POST.get('menu_name')
        target_age = request.POST.get('target_age')
        quantity = request.POST.get('quantity')
        quantity = int(quantity) if quantity else None
        facilities = request.POST.getlist('facility')
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        save_type = request.POST.get('save_type')
        
        post.menu_name = menu_name
        post.target_age = target_age
        post.quantity = quantity
        post.facilities = facilities
        post.rating = rating
        post.content = content
        post.is_draft = True if save_type == 'draft' else False
        post.save()
        
        if post.is_draft:
            return redirect('mypage_drafts')
        
        return redirect('mypage_posts')
    
    return render(request, 'post_edit.html', {
        'post': post,
    })