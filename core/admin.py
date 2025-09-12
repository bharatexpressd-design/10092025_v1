from django.contrib import admin
from .models import Category, Product, Cart

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'material', 'region']
    list_filter = ['category', 'available', 'material', 'region']
    search_fields = ['name', 'description', 'material', 'region']
    prepopulated_fields = {'slug': ('name',)} if 'slug' in [f.name for f in Product._meta.fields] else {}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['user__username', 'product__name']