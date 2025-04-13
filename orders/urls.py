from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.UserOrdersView.as_view(), name='orders'),  # Страница всех заказов
    path('order/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),  # Страница с деталями заказа
]
