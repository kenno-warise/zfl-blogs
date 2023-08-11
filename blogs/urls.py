from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = 'blogs'

urlpatterns = [
        path('', views.index, name='index'),
        path('detail/<int:blog_id>/', views.detail, name='detail'),
        path('new_blog', views.new_blog, name='new_blog'),
        path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
        path('blog_private', views.blog_private, name='blog_private'),
        path('blog_private/private_detail/<int:pk>/',
                    views.private_detail, name='private_detail'),
        path('release/<pk>/', views.release, name='release'),
        path('private/<pk>/', views.private, name='private'),
        path('blogs/<str:category>/', views.blogs_category, name='blogs_category'),
        path('category_graph/', views.category_graph, name='category_graph'),
]

