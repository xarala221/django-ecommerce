from django.urls import path
from . import views

urlpatterns = [
    path("payment-process/", views.payment_process, name="payment-process",),
    path("payment-done/", views.payment_done, name="payment-done",),
    path("payment-canceled/", views.payment_canceled, name="payment-canceled",)
]
