from decimal import Decimal
from django.conf import settings

from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """
        Initialiser le panier
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    # ajouter au panier
    def add(self, product, quantity=1, override_qauntity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0, "price": str(product.price)}
        if override_qauntity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    # supprimer de panier
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # recuperer tous les elements
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item['price'])
            item["total_price"] = item['price'] * item["quantity"]
            yield item

    # compter les elements sur le panier
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # calculer la valeur totale du panier
    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    # vider le panier
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
