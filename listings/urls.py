from django.urls import path
from .views import initiate_payment, verify_payment

urlpatterns = [
    path('payment/initiate/', initiate_payment),
    path('payment/verify/', verify_payment),
]
