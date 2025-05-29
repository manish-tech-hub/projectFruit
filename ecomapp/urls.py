from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('shop/', views.home, name='index'),
    path('search/', views.search, name='search'),
    path('', views.singin),
    path('singin/', views.singin, name='singin'),
    path('singup/', views.singup, name='singup'),
    path('addToCart/<int:product_id>/', views.addToCart, name='addToCart'),
    path('increaseQuantity/<int:item_id>/', views.increaseQuantity, name='increaseQuantity'),
    path('decreaseQuantity/<int:item_id>/', views.decreaseQuantity, name='decreaseQuantity'),
    path('deleteItem/<int:item_id>/', views.deleteItem, name='deleteItem'),
    path('cart/', views.view_cart, name='cart'),
    path('product/<int:product_id>/', views.productdetail, name='productdetail'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.userProfile, name='profile'),
    path('profileupdate/', views.profileupdate, name='profileupdate'),
    path('payment/',views.for_payment,name='payment')
]
