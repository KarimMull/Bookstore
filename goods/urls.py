from django.urls import path

from goods import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('product/<slug:slug>/', views.ProductView.as_view(), name='product'),  # должен быть выше
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
]

