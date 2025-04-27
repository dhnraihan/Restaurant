from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('menu/<slug:slug>/', views.menu_item_detail, name='menu_item_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('reservation/', views.reservation, name='reservation'),
]