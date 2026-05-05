from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post, Favorite, PostKidsMenu
from stores.models import Store

def normalize_menu_name(menu_name):
    if not menu_name:
        return ''
    
    if 'カレー' in menu_name:
        return 'カレー'
    
    if (
        'お子様ランチ' in menu_name
        or 'おこさまランチ' in menu_name
        or 'お子さまランチ' in menu_name
        or 'キッズプレート' in menu_name
    ):
        return 'お子様ランチ'
    
    if 'うどん' in menu_name:
        return 'うどん'
    
    if 'ラーメン' in menu_name:
        return 'ラーメン'
    
    if 'パスタ' in menu_name or 'スパゲッティ' in menu_name or 'スパゲティ' in menu_name:
        return 'パスタ'
    
    if 'パンケーキ' in menu_name or 'ホットケーキ' in menu_name:
        return 'パンケーキ'
    
    if 'オムライス' in menu_name:
        return 'オムライス'
    
    if 'ハンバーガー' in menu_name or 'バーガー' in menu_name:
        return 'ハンバーガー'
    
    if 'ハンバーグ' in menu_name:
        return 'ハンバーグ'
    
    if 'チャーハン' in menu_name or '炒飯' in menu_name:
        return 'チャーハン'
    
    return 'その他'

def create_menu_tags(kids_menus):
    menu_counts = {}
    
    for menu in kids_menus:
        normalized_name = normalize_menu_name(menu.menu_name)
        
        if normalized_name:
            if normalized_name in menu_counts:
                menu_counts[normalized_name] += 1
            else:
                menu_counts[normalized_name] = 1
                
    menu_tags = []
    
    for name, count in menu_counts.items():
        menu_tags.append({
            'name': name,
            'count': count,
        })
        
    return menu_tags
                

def portfolio_top(request): #ポートフォリオトップ画面
    html = """
    <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>KodoMeal</title>
        </head>
        <body>
    
        <h1>KodoMeal</h1> 
        
        <div>
            <p>アプリのスクショ</p> 
        </div>
        
        <div>
            <a href="#">企画書</a>
            <a href="#">画面設計図</a> 
            <a href="#">画面遷移図</a>
            <a href="#">ER図</a>
        </div>
        
        <a href="/kodomeal/" class="app-link-button">このアプリにアクセス</a>
        
    </body>
    </html>
    """
    return HttpResponse(html)

def app_top(request): #アプリトップ画面
    return render(request,'app_top.html')

def search_result(request):  #検索結果画面
    keyword = request.GET.get('keyword')
    selected_menus = request.GET.getlist('menu')
    
    stores = list(
        Store.objects.filter(
            is_closed=False
        ).order_by('id')
    )
    
    if keyword :
        stores = [
            store for store in stores
            if keyword in store.name
            or any(
                keyword in menu['name']
                for menu in store.menu_tags
            )      
        ]
        
    if selected_menus:
        stores = [
            store for store in stores
            if any(
                selected_menu == menu['name']
                for selected_menu in selected_menus
                for menu in store.menu_tags
            )
        ]
    
        for kids_menu in kids_menus:
            normalized_name = normalize_menu_name(kids_menu.menu_name)
            
            if normalized_name in selected_menus:
                matched_store_ids.add(kids_menu.post.store.id)
                
        store = stores.filter(
            id__in=matched_store_ids
        )
    
    for store in stores:
        store.posts_count = Post.objects.filter(
            store=store,
            is_draft=False
        ).count()
        
        kids_menus = PostKidsMenu.objects.filter(
            post__store=store,
            post__is_draft=False
        )
        
        store.menu_tags = create_menu_tags(kids_menus)
        
    if request.user.is_authenticated:
        favorite_store_ids = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list('store_id', flat=True)
        )
    else:
        favorite_store_ids = []
    
    return render(request, 'search_result.html', { #キーワード受け取る
        'keyword': keyword,
        'selected_menus': selected_menus,
        'stores' : stores,
        'favorite_store_ids': favorite_store_ids,
    })
    
def store_detail(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id,
        is_closed=False
    )
    
    posts_count = Post.objects.filter(
        store=store,
        is_draft=False
    ).count()
    
    posts_preview = Post.objects.filter(
        store=store,
        is_draft=False
    ).order_by('-created_at')[:3]
    
    kids_menus = PostKidsMenu.objects.filter(
        post__store=store,
        post__is_draft=False
    ).order_by('-created_at')
    
    menu_tags = create_menu_tags(kids_menus)
    
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            store=store
        ).exists()
    else:
        is_favorite = False
    
    return render(request, 'store_detail.html', { 
        'store' : store,
        'posts_count': posts_count,
        'posts_preview': posts_preview,
        'kids_menus': kids_menus,
        'menu_tags': menu_tags,
        'is_favorite': is_favorite,
    })
    
@login_required
def favorite_list(request):
    favorite_store_ids = list(
        Favorite.objects.filter(
            user=request.user
        ).order_by('-created_at')
        .values_list('store_id', flat=True)
    )
    
    favorites = Store.objects.filter(
        id__in=favorite_store_ids,
        is_closed=False
    )
    
    for store in favorites:
        store.posts_count = Post.objects.filter(
            store=store,
            is_draft=False
        ).count()
    
    return render(request, 'favorite_list.html', {
        'favorites': favorites,
    })
    
@login_required
def toggle_favorite(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id,
        is_closed=False
    )
    
    favorite = Favorite.objects.filter(
        user=request.user,
        store=store
    ).first()
    
    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            store=store
        )
        
    return redirect(request.META.get('HTTP_REFERER', 'favorite_list'))
            