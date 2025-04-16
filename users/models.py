from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    image = models.ImageField(upload_to='user_images/', null=True, blank=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер телефона")

    def __str__(self):
        return self.username
    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username