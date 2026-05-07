from django.contrib import admin
from .models import Store, StoreImage

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone_number')
    ordering = ('-created_at', )

@admin.register(StoreImage)
class StoreImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'image', 'created_at')
    ordering = ('-created_at', )