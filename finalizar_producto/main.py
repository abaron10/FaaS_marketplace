from google.cloud import storage
from os import abort
from flask import jsonify
from variables import SERVER, INTEGRATIONS_SERVER, NOTIFICATIONS_SERVER
import uuid
import json
import requests

def finalizar_producto(request):
    try:
        token = request.headers["x-auth-token"]
        validation_login = requests.get(f"https://{SERVER}/sesion/{token}")
        if validation_login.status_code != 200:
            return validation_login.json(), 401

        request_args = request.args
        order_id = request_args['orderId']
        urlOrder = f'https://{SERVER}/orders/internal/{order_id}'
        update_order = requests.post(urlOrder, data={'state': 'LISTA_PARA_DESPACHO'})

        if update_order.status_code != 200:
            return {'message': 'error actualizando orden'}, 404
        
        # crear entrega pedido (crear agenda)
        dataS={'uuid': str(order_id)}
        seller_id = request_args['sellerId']
        urlAgenda = f'https://{SERVER}/agenda/sellers/{seller_id}'
        update_agenda = requests.post(urlAgenda, json=dataS)
        
        if update_agenda.status_code != 201:
            return {'message': 'error creando agenda'}, 404
        
        #notificar al comprador
        notification_data = {
            "notificacion": 'Su orden ha cambiado de estado a LISTA_PARA_DESPACHO',
            "type": 1,
            "order_id": str(order_id)
        }

        notificador_response = requests.post(
            f'https://{NOTIFICATIONS_SERVER}/funcion-notificaciones-producir',
            json=notification_data
        )
		
        if notificador_response.status_code != 200:
            raise Exception("Error")
		
        #Obtener direccion comprador
        addr_response = requests.post(
            f'https://{SERVER}/addresses/user/{validation_login.json()["user_id"]}'
        )
        
        if addr_response.status_code != 200:
            raise Exception("Error")
		
        #Agendar entrega en proveedor
        #agenda_data = {
        #    "direccion-origen": "Cr 40 #40 - 40, Bogotá, Colombia",
        #    "direccion-destino": addr_response.json()["address"]
        #}
        #update_agenda = requests.post(f'https://{INTEGRATIONS_SERVER}/envio/agendar', json=agenda_data)
		
        #if update_agenda.status_code != 200:
        #    raise Exception("Error")

        return {
            "message": addr_response.json()
        }

    except Exception as e:
        return "error", 400
