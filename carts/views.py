from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products

def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Products.objects.get(id=product_id)
        
        # Если пользователь аутентифицирован
        if request.user.is_authenticated:
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        else:
            # Если пользователь не аутентифицирован, создаем корзину по сессионному ключу
            cart_item, created = Cart.objects.get_or_create(session_key=request.session.session_key, product=product)
        
        # Если товар был добавлен в корзину, увеличиваем его количество
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({
            'message': 'Товар добавлен в корзину!',
        })

def user_cart(request):
    # Получаем все товары в корзине пользователя
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.filter(session_key=request.session.session_key)
    
    # Пересчитываем общую сумму
    total_price = sum([item.products_price() for item in cart_items])
    
    return render(request, 'carts/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def cart_change(request):
    cart_id = request.POST.get('cart_id')
    quantity = int(request.POST.get('quantity'))

    # Получаем корзину
    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()

    # Пересчитываем общую цену
    total_price = sum([item.products_price() for item in Cart.objects.filter(user=request.user)])
    
    response_data = {
        'message': 'Количество изменено',
        'total_price': total_price,
        'cart_items_html': render_to_string('carts/includes/included_cart.html', {'cart_items': Cart.objects.filter(user=request.user)}),
    }
    
    return JsonResponse(response_data)

def cart_remove(request):
    cart_id = request.POST.get('cart_id')
    
    # Получаем корзину и удаляем товар
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    
    # Пересчитываем общую цену
    total_price = sum([item.products_price() for item in Cart.objects.filter(user=request.user)])
    
    response_data = {
        'message': 'Товар удален из корзины',
        'total_price': total_price,
        'cart_items_html': render_to_string('carts/includes/included_cart.html', {'cart_items': Cart.objects.filter(user=request.user)}),
    }
    
    return JsonResponse(response_data)
