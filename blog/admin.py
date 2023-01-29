from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_slug', 'author', 'image']
    search_fields = ['title','subtitle']
    prepopulated_fields = {'category_slug': ('title',)}
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_slug', 'author', 'publish', 'status', 'image']
    list_filter = ['status', 'created',  'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'post_slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']