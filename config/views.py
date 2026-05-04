from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post, Favorite
from stores.models import Store
from django.contrib.auth.decorators import login_required

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
    
    stores = Store.objects.filter(
        is_closed=False
    ).order_by('id')
    
    if keyword :
        stores = stores.filter(
            name__icontains=keyword
        )
        
# TODO: post_kids_menu作成後、選択メニュー検索をDB対応する
    
    for store in stores:
        store.posts_count = Post.objects.filter(
            store_id=store.id,
            is_draft=False
        ).count()
        
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
        store_id=store.id,
        is_draft=False
    ).count()
    
    posts_preview = Post.objects.filter(
        store_id=store.id,
        is_draft=False
    ).order_by('created_at')[:3]
    
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            store_id=store.id
        ).exists()
    else:
        is_favorite = False
    
    return render(request, 'store_detail.html', { 
        'store' : store,
        'posts_count': posts_count,
        'posts_preview': posts_preview,
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
            store_id=store.id,
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
            