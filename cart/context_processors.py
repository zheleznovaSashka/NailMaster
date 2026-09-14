def cart(request):
    """Контекстный процессор для корзины"""
    # У админов корзина не считается
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return {
            'cart_total_items': 0,
            'cart': {},
        }

    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return {
        'cart_total_items': total_items,
        'cart': cart,
    }