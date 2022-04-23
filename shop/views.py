from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View
from django.db.models import Q

from cart.forms import CartAddProductForm

from .models import Category, Product


def index(request):
    products = Product.objects.all()
    context = {"title": "Bienvenue chez vous", "products": products, }
    return render(request, "index.html", context)


class ProductList(View):
    template_name = 'shop/product_list.html'

    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        q = request.GET.get("q")
        request.session["nom"] = "Xarala"
        request.session.get("nom")
        del request.session["nom"]
        if q:
            products = Product.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )
        return render(request, self.template_name, {"products": products, "categories": categories, })


class ProductDetail(DetailView):
    model = Product
    context_object_nme = 'product'
    template_name = 'shop/product_details.html'
    # def get(self, request):
    #     return render(request, self.template_name, {"product": product})

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context
