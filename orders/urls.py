from django.urls import path

from orders.views import order_create, order_created


urlpatterns = [
    path("checkout/", order_create, name="order_create"),
    path("thanks/", order_created, name="order_created")
]
