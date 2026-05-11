from django.contrib import admin
from .models import Store, StoreImage

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'phone_number',
        'latitude',
        'longitude',
        'is_closed',
        'created_at',
        )
    search_fields = ('name', 'address')
    ordering = ('-created_at', )

@admin.register(StoreImage)
class StoreImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'image', 'created_at')
    ordering = ('-created_at', )