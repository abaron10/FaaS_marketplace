import  requests
from flask import jsonify
import json
import os

def actualizacion_estado_pago(request):
        
    url = f'https://0f11-186-84-88-134.ngrok.io/payments/internal/{request.get_json()["extra1"]}'
    # url = f'http://{PAYMENTS_SERVER}/payments/internal/{request["extra1"]}'
    update_pay = requests.post(url, json = {'state': 'ACEPTADOs'})
    if update_pay.status_code != 201:
        return {"msg":"error while processing payment, try later!"},404 
    url = f'https://0f11-186-84-88-134.ngrok.io/orders/internal/{update_pay.json()["orderId"]}'
    update_del = requests.post(url, json = {'state': 'AGENDADOs'})
    if update_del.status_code != 200:
        return {"msg":"error while updating delivery"},404
    
        
    message = {
        "notificacion": "Hola",
        "type": 0,
        "order_id": update_pay.json()["orderId"]
    }

    url = 'https://us-central1-miso-339504.cloudfunctions.net/funcion-notificaciones-producir'
    message = requests.post(url, json = message)
    if message.status_code != 200:
        return {"msg":"error while sending message"},404
    
    return {"msg":"succesfull update"}
    