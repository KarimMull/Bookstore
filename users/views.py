from django.contrib import messages, auth
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from users.models import User
from orders.models import Order

class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("main:index")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                Cart.objects.filter(user=user).delete()
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
            return HttpResponseRedirect(self.get_success_url())

        return super().form_invalid(form)


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Регистрация прошла успешно! Теперь вы можете войти.")
        return response



class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Данные профиля обновлены")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем заказы пользователя в контекст
        user = self.request.user
        context['orders'] = Order.objects.filter(user=user)  # Получаем заказы текущего пользователя
        return context


class UserCartView(TemplateView):
    template_name = "users/users_cart.html"


def logout(request):
    django_logout(request)
    messages.success(request, "Вы вышли из аккаунта")
    return HttpResponseRedirect(reverse_lazy("main:index"))
