from google.cloud import storage
from os import abort
from flask import jsonify
from variables import SERVER, INTEGRATIONS_SERVER, NOTIFICATIONS_SERVER
import uuid
import json
import requests
import ast
import time

def finalizar_producto(request):
    try:
        request_data = request.data
        string_data = request_data.decode('utf8')
        request_args = ast.literal_eval(string_data)

        token = request.headers["x-auth-token"]
        validation_login = requests.get(f"https://{SERVER}/sesion/{token}")

        while validation_login.status_code == 500:
            validation_login = requests.get(f"https://{SERVER}/sesion/{token}")
        if validation_login.status_code != 200:
            return validation_login.json(), 401

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
            return {'message': 'error creando notificacion'}, 404
		
        #Obtener direccion comprador
        idUser=validation_login.json()["user_id"]
        addr_response = requests.get(
            f'https://{SERVER}/addresses/user/{idUser}'
        )
        
        if addr_response.status_code != 200:
            return {'message': 'error obteniendo direccion'}, 404
		
        #Agendar entrega en proveedor
        agenda_data = {
            "direccion-origen": "Cr 40 #40 - 40, Bogotá, Colombia",
            "direccion-destino": addr_response.json()["address"]
        }
        update_agenda = requests.post(f'https://{INTEGRATIONS_SERVER}/envio/agendar', json=agenda_data)
		
        # Reintentos servicio de agenda con el proveedor
        while update_agenda.status_code == 500:
            time.sleep(1)
            update_agenda = requests.post(f'https://{INTEGRATIONS_SERVER}/envio/agendar', json=agenda_data)

        return {
            "message": "Producto finalizado correctamente, se agenda entrega con el proveedor"
        }

    except Exception as e:
        return {"message": "Error en la funcion de finalizar pedido"}, 400
