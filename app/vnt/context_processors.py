from .cart import Cart

def get_total_cart(request):

    Cart(request)
    total = 0
    if request.user:
        for key, value in request.session['cart'].items():
            total = total + (float(value['precio']))

    return {'get_total_cart': total}