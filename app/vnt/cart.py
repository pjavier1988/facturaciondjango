class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):

        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                'id': product.id,
                'name': product.descripcion,
                'cantidad': 1,
                'precio': str(product.precio),
                'imagen': product.imagen.url,
            }
        else:
            for key, value in self.cart.items():
                if key == str(product.id):
                    value['cantidad'] = value['cantidad'] + 1
                    value['precio'] = float(value['precio']) + product.precio
                    break
        self.save()
    
    def save(self):
        self.session['card'] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def decrement(self, product):

        for key, value in self.cart.items():
            if key == str(product.id):
                value['cantidad'] = value['cantidad'] - 1
                value['precio'] = float(value['precio']) - product.precio

                if value['cantidad'] < 1:
                    self.remove(product)
                break

        self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True