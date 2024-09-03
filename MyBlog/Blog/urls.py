"""
URL configuration for MyBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import *


app_name = 'Blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('post/<int:id>/', SinglePostView.as_view(), name='single_post'),
    path('category/<slug:slug>/', CategoryPostsView.as_view(), name='category_posts'),
    path('search/', SearchView.as_view(), name='search'),
    path('create-post/', create_post, name='create_post'),
    path('edit-post/<int:id>/', edit_post, name='edit_post'),
    path('delete-post/<int:id>/', delete_post, name='delete_post'),
]
