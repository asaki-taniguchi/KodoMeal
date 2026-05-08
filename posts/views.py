from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post, PostKidsMenu, PostSeatType
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
        seat_types = request.POST.getlist('seat_type')
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        save_type = request.POST.get('save_type')
        
        is_draft = True if save_type == 'draft' else False
        
        post = Post.objects.create(
            user=request.user,
            store=store,
            menu_name=menu_name,
            target_age=target_age,
            quantity=quantity,
            has_kids_chair=request.POST.get('has_kids_chair') == '1',
            has_diaper_table=request.POST.get('has_diaper_table') == '1',
            has_kids_space=request.POST.get('has_kids_space') == '1',
            has_kids_cutlery=request.POST.get('has_kids_cutlery') == '1',
            is_stroller_ok=request.POST.get('is_stroller_ok') == '1',
            content=content,
            rating=rating,
            is_draft=is_draft
        )
        
        for seat_type in seat_types:
            PostSeatType.objects.create(
                post=post,
                seat_type=int(seat_type)
            )
        
        if menu_name or target_age or quantity:
            PostKidsMenu.objects.create(
                post=post,
                menu_name=menu_name,
                target_age=target_age,
                quantity=quantity
            )
        
        return redirect('store_detail', store_id=store.id)
    
    return render(request, 'post_create.html', {
        'store': store
    })

def post_list(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id,
        is_closed=False
    )
    
    posts = Post.objects.filter(
        store=store,
        is_draft=False
        ).order_by('-created_at')
    
    return render(request, 'post_list.html', {
        'store': store,
        'posts': posts
    })

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
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
        
        post.menu_name = menu_name
        post.target_age = target_age
        post.quantity = quantity
        post.facilities = facilities
        post.rating = rating
        post.content = content
        post.is_draft = True if save_type == 'draft' else False
        post.save()
        
        if menu_name or target_age or quantity:
            PostKidsMenu.objects.update_or_create(
                post=post,
                defaults={
                    'menu_name': menu_name,
                    'target_age': target_age,
                    'quantity': quantity,
                }
            )
        
        if post.is_draft:
            return redirect('mypage_drafts')
        
        return redirect('mypage_posts')
    
    return render(request, 'post_edit.html', {
        'post': post,
    })