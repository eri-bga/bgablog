from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<category>', views.category, name='category'),
    path('tag/<slug:tag_slug>', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
        views.post_detail, 
        name='post_detail'),
    path('<int:post_id>', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('new_category/', views.new_category, name='category_create'),
    path('new_post/', views.new_post, name='post_create'),
    path('<category>/update', views.category_update, name='category_update'),
    path('<category>/delete', views.category_delete, name='category_delete'),
    path('<category>/<post>/update', views.post_update, name='post_update'),
    path('<category>/<post>/delete', views.post_delete, name='post_delete'),
    path('<category>/<post>/upload_image', views.upload_image, name='upload_image'),
    path('newsletter/', views.newsletter, name='newsletter'),
]
