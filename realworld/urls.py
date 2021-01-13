"""realworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from home import views as home_views
from articles import views as articles_views
from profiles import views as profile_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_views.index, name="index"),
    path("article/<slug:slug>/", articles_views.ViewArticle.as_view(), name="article_view"),
    path("article/<slug:slug>/add_comment", articles_views.AddComment.as_view(), name="add_comment"),
    path("article/comment/login_to_add/<slug:slug>", articles_views.LoginToAddComment.as_view(), name="login_to_add_comment"),
    path("article/comment/<int:pk>", articles_views.ViewComment.as_view(), name="view_comment"),
    path("article/comment/<int:pk>/edit", articles_views.EditComment.as_view(), name="edit_comment"),
    path("article/comment/<int:pk>/delete", articles_views.DeleteComment.as_view(), name="delete_comment"),
    path("article/comment/<int:pk>/deleted", articles_views.DeletedComment.as_view(), name="deleted_comment"),
    path("article/", articles_views.ListArticle.as_view(), name="article_list"),    
    path("editor/<slug:slug>/", articles_views.EditArticle.as_view(), name="article_edit"),
    path("editor/", articles_views.CreateArticle.as_view(), name="article_create"),
    path("@<slug:profile>/", profile_views.view, name="profile_view"),
    path("settings/", profile_views.edit, name="profile_edit"),
    path("register/", home_views.signup, name="signup"),
    path("login/", home_views.LoginView.as_view(), name="login"),
]
