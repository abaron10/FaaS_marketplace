from google.cloud import storage
from os import abort
from flask import jsonify
import env_vars as env
import uuid
import json
import requests

def estimar_fecha_finalizacion(request):
    try:
        base_url = env.get_base_url()
        request_args = request.args
        order_id = request_args['id']
        data = {
            "state": "ENTREGADA"
        }
        order_response = requests.post(
            f'{base_url}/orders/internal/{order_id}',
            json=data
        )

        if order_response.status_code != 200:
            raise Exception("Error")

        # TODO: Notificar al comprador
        return { "message": "Se notifico al comprador correctamente" }
    except Exception as e:
        return "Oops, hubo un error", 400
