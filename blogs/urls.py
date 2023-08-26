from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = 'blogs'

urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
        path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
        path('private_index/', views.PrivateIndexView.as_view(), name='private_index'),
        path('new_blog', views.new_blog, name='new_blog'),
        path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
        path('private_index/private_detail/<int:pk>/',
                    views.private_detail, name='private_detail'),
        path('release/<pk>/', views.release, name='release'),
        path('private/<pk>/', views.private, name='private'),
        path('category_graph/', views.category_graph, name='category_graph'),
]

