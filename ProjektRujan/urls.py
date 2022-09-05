"""ProjektRujan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from Application import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'Application'
urlpatterns = [
    path('',views.home),
    path('admin/', admin.site.urls),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    ####ADMIN PAGE
    path('users/', views.users_list_all, name='user_list_all'),
    path('users_profesors/', views.users_list_by_profesors, name='user_list_profesor'),
    path('users_students/', views.users_list_by_students, name='user_list_student'),
    path('user_create/', views.create_user, name='create_user'),
    path('user_edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user_delete/<int:user_id>/', views.delete_user, name='delete_user'),
    ####PROFESOR PAGE
    path('upload/', views.upload, name='file_upload'),
    path('document_list/', views.document_list, name='document_list'),
    path('document_list_by_name/', views.document_list_by_name, name='document_list_by_name'),
    path('document_share/<int:document_id>/', views.share_document, name='share_document'),
    path('document_stop_share/<int:document_id>/', views.stop_share_document, name='stop_share_document'),
    path('document_delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('profesor_document_list/<int:user_id>/', views.profesor_document_list, name='profesor_document_list'),
    path('rujan/', views.rujan, name='rujan'),
    path('document_page/<int:user_id>/', views.document_page, name='document_page'),
    path('document_edit/<int:document_id>/', views.document_edit, name='document_edit'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
