# catalog/admin.py
from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'publish_status')  # Добавляем столбец с статусом публикации
    list_filter = ('category', 'publish_status')  # Добавляем фильтр по статусу публикации
    search_fields = ('name', 'description')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
