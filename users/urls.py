from django.urls import path
from users import views

app_name = 'users'  # именно 'users', не 'user'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('cart/', views.UserCartView.as_view(), name='users_cart'), 
]
