from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.user_cart, name='user_cart'),  # Страница корзины
    path('add/', views.cart_add, name='cart_add'),  # Добавление товара в корзину
    path('cart_change/', views.cart_change, name='cart_change'),  # Изменение количества товара
    path('cart_remove/', views.cart_remove, name='cart_remove'),  # Удаление товара
]
