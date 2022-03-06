from variables import PAYMENTS_SERVER ,ORDERS_SERVER
import  requests
from flask import jsonify
import json
import os

def actualizacion_estado_pago(request):
    def update_payment():
        # url = f'http://{get_payments_url()}/payments/internal/d1fb723f-fc94-4f3e-a486-e7340bd87ec2'
        url = f'http://{PAYMENTS_SERVER}/payments/internal/{request.json()["extra1"]}'
        update_pay = requests.post(url, json = {'state': 'ACEPTADO'})
        if update_pay.status_code != 201:
            return {"msg":"error while processing payment, try later!"},404 
        return update_pay

    def update_delivery(payment_info):

        print(type(payment_info))
        
        url = f'http://{get_orders_url()}/orders/internal/{payment_info.json()["orderId"]}'
        update_del = requests.post(url, data = {'state': 'AGENDADO'})
        if update_del.status_code != 200:
            return {"msg":"error while updating delivery"},404
        return update_del

    payment_process = update_delivery(update_payment())

    if payment_process.status_code == 200:
        return {"msg":"succesfull update"}

def get_payments_url():
    return os.environ.get("PAYMENTS_SERVER","")
    
def get_orders_url():
    return os.environ.get("ORDERS_SERVER","")
    
print(actualizacion_estado_pago())


