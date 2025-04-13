from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import TemplateView
from orders.models import Order, OrderItem

# Страница с заказами пользователя
class UserOrdersView(LoginRequiredMixin, TemplateView):
    template_name = "orders/orders_list.html"  # Шаблон для списка заказов

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['orders'] = Order.objects.filter(user=user)  # Получаем все заказы текущего пользователя
        return context

# Детали конкретного заказа
class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = "orders/order_detail.html"  # Шаблон для деталей заказа

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']

        # Получаем заказ по ID и проверяем, принадлежит ли он текущему пользователю
        try:
            order = Order.objects.get(id=order_id, user=self.request.user)
            order_items = OrderItem.objects.filter(order=order)
        except Order.DoesNotExist:
            raise Http404("Заказ не найден или не принадлежит этому пользователю")

        context['order'] = order
        context['order_items'] = order_items
        return context
