from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post, PostKidsMenu, PostSeatType, PostImage
from stores.models import Store

@login_required
def post_create(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id,
        is_closed=False
    )
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        menu_name = request.POST.get('menu_name')
        target_age = request.POST.get('target_age')
        quantity = request.POST.get('quantity')
        quantity = int(quantity) if quantity else None
        seat_types = request.POST.getlist('seat_type')
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        save_type = request.POST.get('save_type')
        errors = {}

        if save_type == 'publish' and not images:
            errors['image_error'] = '写真は1枚以上登録してください。'

        if len(images) > 4:
            errors['image_error'] = '写真は最大4枚まで投稿できます。'

        if save_type == 'publish' and not rating:
            errors['rating_error'] = '総合評価をしてください。'

        if errors:
            return render(request, 'post_create.html', {
                'store': store,
                **errors,
            })      
        
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
            
        for image in images:
            PostImage.objects.create(
                post=post,
                image=image
            )
            
        if post.is_draft:
            messages.success(request, '下書き保存しました')
            return redirect('mypage_drafts')
    
        messages.success(request, '投稿完了しました')
        return redirect('store_detail', store_id=store.id)

    return render(request, 'post_create.html', {
        'store': store
    })

def post_list(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id,
    )
    
    sort = request.GET.get('sort', 'new')
    
    posts = Post.objects.filter(
        store=store,
        is_draft=False
        )
    
    if sort == 'old':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')
    
    return render(request, 'post_list.html', {
        'store': store,
        'posts': posts,
        'sort': sort,
    })
    
def build_post_edit_context(post, error_message=None):
    post_images = post.images.all()
    empty_slot_count = max(0, 4 - post_images.count())
    
    return {
        'post': post,
        'selected_seat_types': list(
            post.seat_types.values_list('seat_type', flat=True)
        ),
        'post_images': post_images,
        'empty_slots': range(empty_slot_count),
        'error_message': error_message,
    }

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
        seat_types = request.POST.getlist('seat_type')
        delete_image_ids = request.POST.getlist('delete_images')
        add_images = request.FILES.getlist('add_images')
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        save_type = request.POST.get('save_type')
        
        current_image_count = post.images.count()
        
        delete_image_count = PostImage.objects.filter(
            id__in=delete_image_ids,
            post=post
        ).count()
        
        add_image_count = len(add_images)
        
        final_image_count = current_image_count - delete_image_count + add_image_count
        
        if final_image_count < 1:
            return render(
                request,
                'post_edit.html',
                build_post_edit_context(
                    post,
                    '写真は1枚以上登録してください。'
                )
            )
            
        if final_image_count > 4:
            return render(
                request,
                'post_edit.html',
                build_post_edit_context(
                    post,
                    '写真は最大4枚まで投稿できます。'
                )
            )
        
        post.menu_name = menu_name
        post.target_age = target_age
        post.quantity = quantity
        post.has_kids_chair = request.POST.get('has_kids_chair') == '1'
        post.has_diaper_table = request.POST.get('has_diaper_table') == '1'
        post.has_kids_space = request.POST.get('has_kids_space') == '1'
        post.has_kids_cutlery = request.POST.get('has_kids_cutlery') == '1'
        post.is_stroller_ok = request.POST.get('is_stroller_ok') == '1'
        post.rating = rating
        post.content = content
        post.is_draft = True if save_type == 'draft' else False
        post.save()
        
        delete_images = PostImage.objects.filter(
            id__in=delete_image_ids,
            post=post
        )
        
        delete_image_id_set = set(
            delete_images.values_list('id', flat=True)
        )
        
        delete_images.delete()
        
        for post_image in post.images.all():
            if post_image.id in delete_image_id_set:
                continue
            
            replace_image = request.FILES.get(f'replace_image_{post_image.id}')
            
            if replace_image:
                post_image.image = replace_image
                post_image.save()
                
        for image in add_images:
            PostImage.objects.create(
                post=post,
                image=image
            )
        
        post.seat_types.all().delete()
        
        for seat_type in seat_types:
            PostSeatType.objects.create(
                post=post,
                seat_type=int(seat_type)
            )
        
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
            messages.success(request, '下書き保存しました')
            return redirect('mypage_drafts')
        
        messages.success(request, '更新完了しました')
        return redirect('mypage_posts')
    
    return render(request, 'post_edit.html', build_post_edit_context(post))

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )
    
    if request.method == 'POST':
        is_draft = post.is_draft
        
        post.delete()
        
        if is_draft:
            return redirect('mypage_drafts')
        
        return redirect('mypage_posts')
    
    return redirect('post_edit', post_id=post.id)