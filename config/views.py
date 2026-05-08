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

def create_facility_tags(posts):
    facility_labels = {
        'stroller': 'ベビーカーOK',
        'kids_chair': 'キッズチェア',
        'diaper': 'おむつ交換台',
        'kids_space': 'キッズスペース',
        'kids_cutlery': 'キッズカトラリー',
    }
    
    seat_type_labels = {
        'private_room': '個室',
        'tatami': '座敷',
        'table': 'テーブル',
    }
    
    posts = list(posts)
    total_count = len(posts)
    
    facility_counts = {}
    seat_type_counts = {}
    
    for post in posts:
        for facility in post.facilities:
            if facility in facility_labels:
                facility_counts[facility] = facility_counts.get(facility, 0) + 1
                
            if facility in seat_type_labels:
                seat_type_counts[facility] = seat_type_counts.get(facility, 0) + 1
            
    facility_tags = []
    
    for key, label in facility_labels.items():
        count = facility_counts.get(key, 0)
        percentage = count / total_count if total_count > 0 else 0
        
        facility_tags.append({
            'key': key,
            'label': label,
            'count': count,
            'is_active': percentage >= 0.5,
        })
        
    seat_type_tags = []
    
    for key, label in seat_type_labels.items():
        count = seat_type_counts.get(key, 0)
        percentage = count / total_count if total_count > 0 else 0
        
        seat_type_tags.append({
            'key': key,
            'label': label,
            'count': count,
            'is_active': percentage >= 0.5,
        })
        
    return facility_tags, seat_type_tags

def store_matches_facilities(store, selected_facilities):
    if not selected_facilities:
        return True
    
    published_posts = Post.objects.filter(
        store=store,
        is_draft=False
    )
    
    published_posts = list(published_posts)
    total_count = len(published_posts)
    
    if total_count == 0:
        return False
    
    facility_counts = {}
    
    for post in published_posts:
        for facility in post.facilities:
            if facility in facility_counts:
                facility_counts[facility] += 1
            else:
                facility_counts[facility] = 1

    for selected_facility in selected_facilities:
        count = facility_counts.get(selected_facility, 0)
        percentage = count/total_count
        
        if percentage < 0.5:
            return False
        
    return True

def get_facility_label(facility_key):
    facility_labels = {
        'stroller': 'ベビーカーOK',
        'kids_chair': 'キッズチェア',
        'diaper': 'おむつ交換台',
        'kids_space': 'キッズスペース',
        'kids_cutlery': 'キッズカトラリー',
        'private_room': '個室',
        'tatami': '座敷',
        'table': 'テーブル',
    }
    
    return facility_labels.get(facility_key, facility_key)

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
    selected_facilities = request.GET.getlist('facility')
    sort = request.GET.get('sort', 'new')
    
    selected_facility_labels = []
    
    for facility in selected_facilities:
        selected_facility_labels.append(get_facility_label(facility))
    
    if sort == 'old':
        stores = list(
            Store.objects.filter(
                is_closed=False
            ).order_by('created_at')
        )
    else:
        stores = list(
            Store.objects.filter(
                is_closed=False
            ).order_by('-created_at')
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
        store.main_image = store.images.first()
    
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
        
    if selected_facilities:
        stores = [
            store for store in stores
            if store_matches_facilities(store, selected_facilities)
        ]
        
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
        'selected_facilities': selected_facilities,
        'selected_facility_labels': selected_facility_labels,
        'stores' : stores,
        'favorite_store_ids': favorite_store_ids,
        'sort': sort,
    })
    
def store_detail(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id,
        is_closed=False
    )
    
    published_posts = Post.objects.filter(
        store=store,
        is_draft=False
    )
    
    posts_count = published_posts.count()
    
    posts_preview = published_posts.order_by('-created_at')[:3]
    
    kids_menus = PostKidsMenu.objects.filter(
        post__store=store,
        post__is_draft=False
    ).order_by('-created_at')
    
    menu_tags = create_menu_tags(kids_menus)
    
    facility_tags, seat_type_tags = create_facility_tags(published_posts)
    
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
        'facility_tags': facility_tags,
        'seat_type_tags': seat_type_tags,
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
        
        store.main_image = store.images.first()
    
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
            