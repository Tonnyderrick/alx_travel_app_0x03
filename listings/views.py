from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import Payment
import requests
import uuid

@api_view(['POST'])
def initiate_payment(request):
    data = request.data
    booking_reference = str(uuid.uuid4())
    amount = data.get("amount")
    
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    payload = {
        "amount": amount,
        "currency": "ETB",
        "email": data.get("email"),
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "tx_ref": booking_reference,
        "callback_url": "http://localhost:8000/api/payment/verify/"
    }

    response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        checkout_url = response_data["data"]["checkout_url"]
        Payment.objects.create(
            booking_reference=booking_reference,
            amount=amount,
            transaction_id=response_data["data"]["tx_ref"]
        )
        return Response({"checkout_url": checkout_url})
    return Response({"error": "Payment initiation failed"}, status=400)

@api_view(['GET'])
def verify_payment(request):
    tx_ref = request.GET.get('tx_ref')
    response = requests.get(
        f"https://api.chapa.co/v1/transaction/verify/{tx_ref}",
        headers={"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
    )

    if response.status_code == 200:
        status = response.json()['data']['status']
        payment = Payment.objects.get(transaction_id=tx_ref)
        payment.status = 'Completed' if status == 'success' else 'Failed'
        payment.save()
        return Response({"status": payment.status})
    return Response({"error": "Verification failed"}, status=400)
