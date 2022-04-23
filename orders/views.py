
from django.shortcuts import redirect, render

from orders.models import OrderItem
from send_mail.views import send_new_order_email, send_new_order_email_with_template
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            email = form.cleaned_data.get("email")
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            request.session["order_id"] = order.id
            # on envoi un mail au client
            send_new_order_email(email)
            # send_new_order_email_with_template(email)
            return redirect("payment-process")
        else:
            print("Form", form.errors)
    else:
        form = OrderCreateForm()
    return render(request, "orders/create.html", {"order_cart": cart, "form": form, })


def order_created(request):
    return render(request, "orders/created.html")
