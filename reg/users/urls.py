from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('search', views.search, name='search'),
    path('quota', views.quota, name='quota'),
    path('add_quota', views.add_quota, name='add_quota'),
    path('remove_quota', views.remove_quota, name='remove_quota'),
    path('admin', views.admin, name='admin'),
    path('detail', views.detail, name='detail'),
    path('search_admin', views.search_admin, name='search_admin')
]