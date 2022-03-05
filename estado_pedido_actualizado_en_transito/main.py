from variables import ORDERS_SERVER
import requests


def actualizacion_estado_pedido_en_transito(request=None):
    url = f'http://{ORDERS_SERVER}/orders/internal/{request.get_json()["orderId"]}'
    update_del = requests.post(url, data={'state': 'EN_TRANSITO'})
    if update_del.status_code != 200:
        return {"msg": "error while updating delivery"}, 404
    else:
        return {"msg": "succesfull update"}
