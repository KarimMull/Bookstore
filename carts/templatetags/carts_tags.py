from django import template
from carts.models import Cart

register = template.Library()


@register.simple_tag()
def user_carts(request):
    user = getattr(request, "user", None)
    if hasattr(user, "is_authenticated") and user.is_authenticated:
        return Cart.objects.filter(user=user)
    return Cart.objects.none()  # безопасно вернуть пустой QuerySet
