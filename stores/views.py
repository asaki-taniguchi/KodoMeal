from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Store, StoreImage
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
