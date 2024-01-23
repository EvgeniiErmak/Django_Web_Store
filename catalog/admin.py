# catalog/admin.py
from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'publish_status')  # Добавляем столбец с статусом публикации
    list_filter = ('category', 'publish_status')  # Добавляем фильтр по статусу публикации
    search_fields = ('name', 'description')
    actions = ['make_published', 'make_draft', 'make_archived']

    def make_published(modeladmin, request, queryset):
        queryset.update(publish_status='published')

    def make_draft(modeladmin, request, queryset):
        queryset.update(publish_status='draft')

    def make_archived(modeladmin, request, queryset):
        queryset.update(publish_status='archived')

    make_published.short_description = 'Опубликовать выбранные продукты'
    make_draft.short_description = 'Перевести выбранные продукты в черновик'
    make_archived.short_description = 'Архивировать выбранные продукты'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
