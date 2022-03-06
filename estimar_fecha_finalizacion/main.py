from google.cloud import storage
from os import abort
from flask import jsonify
import env_vars as env
import uuid
import json
import requests
from datetime import timedelta, date
import ast

def estimar_fecha_finalizacion(request):
    try:
        base_url = env.get_base_url()

        token = request.headers["x-auth-token"]
        validation_login = requests.get(f"{base_url}/sesion/{token}")

        while validation_login.status_code == 500:
            validation_login = requests.get(f"{base_url}/sesion/{token}")

        if validation_login.status_code != 200:
            return validation_login.json(), 401

        request_data = request.data
        string_data = request_data.decode('utf8')
        dict_data = ast.literal_eval(string_data)
        order_id = dict_data['id']

        data = {
            "state": "PENDIENTE_DE_FINALIZACION"
        }
        order_response = requests.post(
            f'{base_url}/orders/internal/{order_id}',
            json=data
        )

        if order_response.status_code != 200:
            raise Exception("Error")

        estimated_fabrication = str(date.today() + timedelta(days=1))
        notification_data = {
            "notificacion": f"La fecha estimada de tu envio es {estimated_fabrication}",
            "type": 1,
            "order_id": str(order_id)
        }
        print(notification_data)
        notificador_response = requests.post(
            'https://us-central1-miso-339504.cloudfunctions.net/funcion-notificaciones-producir',
            json=notification_data
        )

        if notificador_response.status_code != 200:
            raise Exception("Error")

        return {
            "message": "Se notificará al comprador con la fecha estimada de finalización"
        }
    except Exception as e:
        print(e)
        return "Oops, hubo un error", 400
