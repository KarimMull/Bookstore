from django.db import models
from django.conf import settings  # используем для ссылок на кастомного пользователя
from goods.models import Products


class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,   # ✅ всегда используем через settings
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        to=Products,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество'
    )
    session_key = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    objects = CartQueryset().as_manager()

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        user_display = self.user.username if self.user else "Аноним"
        return f'Корзина {user_display} | Товар {self.product.name} | Количество {self.quantity}'
