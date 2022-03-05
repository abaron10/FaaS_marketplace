from variables import PAYMENTS_SERVER ,ORDERS_SERVER
import  requests
from flask import jsonify
import json


def actualizacion_estado_pago(request=None):
    def update_payment():
        url = f'http://{PAYMENTS_SERVER}/payments/internal/d1fb723f-fc94-4f3e-a486-e7340bd87ec2'
        # url = f'http://{PAYMENTS_SERVER}/payments/internal/{request["extra1"]}'
        update_pay = requests.post(url, data = {'state': 'ACEPTADO'})
        if update_pay.status_code != 201:
            return {"msg":"error while processing payment, try later!"},404 
        return update_pay

    def update_delivery(payment_info):
        
        url = f'http://{ORDERS_SERVER}/orders/internal/{payment_info.json()["orderId"]}'
        update_del = requests.post(url, data = {'state': 'AGENDADO'})
        if update_del.status_code != 200:
            return {"msg":"error while updating delivery"},404
        return update_del

    payment_process = update_delivery(update_payment())

    if payment_process.status_code == 200:
        return {"msg":"succesfull update"}

    

print(actualizacion_estado_pago())


