def cart(request):
    """Контекстный процессор для корзины"""
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return {
        'cart_total_items': total_items,
        'cart': cart,
    }