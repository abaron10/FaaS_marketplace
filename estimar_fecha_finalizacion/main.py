from google.cloud import storage
from os import abort
from flask import jsonify
import env_vars as env
import uuid
import json
import requests
from datetime import timedelta, date

def estimar_fecha_finalizacion(request):
    try:
        base_url = env.get_base_url()
        request_args = request.args
        order_id = request_args['id']
        data = {
            "state": "PENDIENTE_DE_FINALIZACION"
        }
        order_response = requests.post(
            f'{base_url}/orders/internal/{order_id}',
            json=data
        )

        if order_response.status_code != 200:
            raise Exception("Error")

        estimated_fabrication = date.today() + timedelta(days=1)
        # TODO: Notificar al comprador
        return {
            "message": "Se notificará al comprador con la fecha estimada de finalización"
        }
    except Exception as e:
        return "Oops, hubo un error", 400
