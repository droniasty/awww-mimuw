"""awwwlab URL Configuration

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
# from django import views
from django.contrib import admin
from django.urls import include, path
from awwwapp import views

app_name = 'awwwapp'

urlpatterns = [
    path('', views.login_viev, name='login'),
    path('register_viev/', views.register_viev, name='registerviev'),
    path('login/', views.login, name='loginn'),
    path('frontend/', views.frontend, name='frontend'),
    path('register/', views.register, name='register'),
    #path('', include(('awwwapp.urls', 'awwwapp'), namespace='awwwapp')),
    #path('change_standard/', views.change_standard_view, name='change_standard'),
    path('frontend/change_standard/', views.change_standard, name='change_standard_view'),
    path('frontend/change_processor/', views.change_processor, name='change_processor'),
    path('frontend/change_optimization/', views.change_optimizations, name='change_optimization'),
    path('frontend/change_specyfic/', views.change_specyfic, name='change_specyfic'),
    #path('change_compiler_options/', views.change_compiler_options_view, name='change_compiler_options'),
    path('frontend/add_file/', views.add_file_view, name='add_file'),
    path('frontend/add_catalog/', views.create_catalog_viev, name='add_catalog'),
    path('frontend/change_catalog/', views.change_selected_catalog_id, name='change_catalog'),
    path('frontend/change_file/', views.change_file_id, name='change_file'),
    path('frontend/delete_file/', views.delete_file, name='delete_file'),
    path('frontend/delete_catalog/', views.delete_catalog, name='delete_catalog'),
    path('frontend/program_code/', views.program_code_view, name='program_code'),
    path('change_sections/', views.change_sections_view, name='change_sections'),
    path('user_catalogs/', views.user_catalogs, name='user_catalogs'),
    path('api/get_code/', views.get_code, name='get_code'),
    path('frontend/get_selected/', views.get_selected, name='get_selected'),
]
