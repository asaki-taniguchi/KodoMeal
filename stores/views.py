from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse

from .models import Store, StoreImage
from .utils import get_lat_lng_from_address
from posts.models import Post, Favorite, PostKidsMenu


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
        
        if len(images) > 4:
            return render(request, 'store_register.html', {
                'error_message': '写真は最大4枚まで登録できます。',
                'name': name,
                'address': address,
                'phone_number': phone_number,
                'business_hours': business_hours,
                'regular_holiday': regular_holiday,
                'parking_comment': parking_comment,
            })
        
        if not images :
            return render(request, 'store_register.html', {
                'error_message': '写真は1枚以上登録してください。',
                'name': name,
                'address': address,
                'phone_number': phone_number,
                'business_hours': business_hours,
                'regular_holiday': regular_holiday,
                'parking_comment': parking_comment,
            })
        
        if not name or not address:
            return render(request, 'store_register.html',{
                'error_message': '店舗名・住所は必須です。',
                'name': name,
                'address': address,
                'phone_number': phone_number,
                'business_hours': business_hours,
                'regular_holiday': regular_holiday,
                'parking_comment': parking_comment,
            })
            
        if Store.objects.filter(name=name, address=address).exists():
            return render(request, 'store_register.html', {
                'error_message': '同じ店舗名・住所の店舗はすでに登録されています。',
                'name': name,
                'address': address,
                'phone_number': phone_number,
                'business_hours': business_hours,
                'regular_holiday': regular_holiday,
                'parking_comment': parking_comment,
            })
            
        try:
            latitude, longitude = get_lat_lng_from_address(address)
        except ValueError:
            return render(request, 'store_register.html', {
                'error_message': '住所から位置情報を取得できませんでした。実在する住所を番地まで入力してください。',
                'name': name,
                'address': address,
                'phone_number': phone_number,
                'business_hours': business_hours,
                'regular_holiday': regular_holiday,
                'parking_comment': parking_comment,
            })
            
        has_parking = False
        
        if parking_comment and parking_comment != 'なし':
            has_parking = True
            
        store = Store.objects.create(
            user=request.user,
            name=name,
            address=address,
            latitude=latitude,
            longitude=longitude,
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
    facility_definitions = [
        {
            'key': 'stroller',
            'label': 'ベビーカーOK',
            'field': 'is_stroller_ok',
        },
        {
            'key': 'kids_chair',
            'label': 'キッズチェア',
            'field': 'has_kids_chair',
        },
        {
            'key': 'diaper',
            'label': 'おむつ交換台',
            'field': 'has_diaper_table',
        },
        {
            'key': 'kids_space',
            'label': 'キッズスペース',
            'field': 'has_kids_space',
        },
        {
            'key': 'kids_cutlery',
            'label': 'キッズカトラリー',
            'field': 'has_kids_cutlery',
        },
    ]
    
    seat_type_labels = {
        1: '座敷',
        2: 'テーブル',
        3: '個室',
    }
    
    posts = list(posts)
    total_count = len(posts)
    
    facility_tags = []
    
    for facility in facility_definitions:
        count = 0
        
        for post in posts:
            if getattr(post, facility['field']):
                count += 1
        
        percentage = count / total_count if total_count > 0 else 0
        
        facility_tags.append({
            'key': facility['key'],
            'label': facility['label'],
            'count': count,
            'is_active': percentage >= 0.5,
        })
            
    seat_type_tags = []
    
    for seat_type, label in seat_type_labels.items():
        count = 0
        
        for post in posts:
            selected_seat_types = {
                post_seat_type.seat_type
                for post_seat_type in post.seat_types.all()
            }
        
            if seat_type in selected_seat_types:
                count += 1
            
        percentage = count / total_count if total_count > 0 else 0
        
        seat_type_tags.append({
            'key': seat_type,
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
    ).prefetch_related('seat_types')
    
    published_posts = list(published_posts)
    total_count = len(published_posts)
    
    if total_count == 0:
        return False
    
    facility_field_map = {
        'stroller': 'is_stroller_ok',
        'kids_chair': 'has_kids_chair',
        'diaper': 'has_diaper_table',
        'kids_space': 'has_kids_space',
        'kids_cutlery': 'has_kids_cutlery',
    }
    
    seat_type_map = {
        'tatami': 1,
        'table': 2,
        'private_room': 3,
    }
    
    for selected_facility in selected_facilities:
        count = 0
        
        if selected_facility in facility_field_map:
            field_name = facility_field_map[selected_facility]
            
            for post in published_posts:
                if getattr(post, field_name):
                    count += 1
                    
        elif selected_facility in seat_type_map:
            seat_type_value = seat_type_map[selected_facility]
            
            for post in published_posts:
                selected_seat_types = {
                    post_seat_type.seat_type
                    for post_seat_type in post.seat_types.all()
                }
                
                if seat_type_value in selected_seat_types:
                    count += 1
                    
        else:
            return False

        percentage = count / total_count
        
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
            Store.objects.all().order_by('created_at')
        )
    else:
        stores = list(
            Store.objects.all().order_by('-created_at')
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
        
    map_stores = []
    
    for store in stores:
        if store.latitude is not None and store.longitude is not None:
            map_stores.append({
                'id': store.id,
                'name': store.name,
                'latitude': float(store.latitude),
                'longitude': float(store.longitude),
                'detail_url': reverse('store_detail', args=[store.id]),
            })
        
    return render(request, 'search_result.html', { #キーワード受け取る
        'keyword': keyword,
        'selected_menus': selected_menus,
        'selected_facilities': selected_facilities,
        'selected_facility_labels': selected_facility_labels,
        'stores' : stores,
        'map_stores': map_stores,
        'favorite_store_ids': favorite_store_ids,
        'sort': sort,
        'google_maps_js_api_key': settings.GOOGLE_MAPS_JS_API_KEY,
        'google_maps_map_id': settings.GOOGLE_MAPS_MAP_ID,
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
    ).prefetch_related('seat_types')
    
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
        'google_maps_js_api_key': settings.GOOGLE_MAPS_JS_API_KEY,
        'google_maps_map_id': settings.GOOGLE_MAPS_MAP_ID,
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
            
@login_required
def store_edit_view(request, store_id):
    store = get_object_or_404(
        Store, 
        id=store_id
    )
    
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        business_hours = request.POST.get('business_hours')
        regular_holiday = request.POST.get('regular_holiday')
        parking_comment =request.POST.get('parking_comment')
        
        if not name or not address:
            return render(request, 'store_edit.html', {
                'store': store,
                'error_message': '店舗名・住所は必須です。'
            })
            
        if Store.objects.filter(name=name, address=address).exclude(id=store.id).exists():
            return render(request, 'store_edit.html', {
                'store': store,
                'error_message': '同じ店舗名・住所の店舗はすでに登録されています。'
            })
            
        if address != store.address:
            try:
                latitude, longitude = get_lat_lng_from_address(address)
            except ValueError:
                return render(request, 'store_edit.html', {
                    'store': store,
                    'error_message': '住所から位置情報を取得できませんでした。実在する住所を番地まで入力してください。',
                })
                
            store.latitude = latitude
            store.longitude = longitude
            
        has_parking = False
        
        if parking_comment and parking_comment != 'なし':
            has_parking = True
            
        store.name = name
        store.address = address
        store.phone_number = phone_number
        store.business_hours = business_hours
        store.regular_holiday = regular_holiday
        store.has_parking = has_parking
        store.parking_comment = parking_comment
        store.save()
        
        return redirect('store_detail', store_id=store.id)
    
    return render(request, 'store_edit.html', {
        'store': store
    })
    
@login_required
def store_toggle_closed_view(request, store_id):
    store = get_object_or_404(
        Store,
        id=store_id
    )
    
    if request.method == 'POST':
        store.is_closed = not store.is_closed
        store.save()
        
        return redirect('store_edit', store_id=store.id)
    
    return redirect('store_edit', store_id=store.id)