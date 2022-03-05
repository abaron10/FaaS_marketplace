from variables import ORDERS_SERVER
import requests


def actualizacion_estado_pedido_en_transito(request=None):
    def update_delivery(payment_info=None):
        url = f'http://{ORDERS_SERVER}/orders/internal/{payment_info.json()["orderId"]}'
        update_del = requests.post(url, data={'state': 'EN_TRANSITO'})
        if update_del.status_code != 200:
            return {"msg": "error while updating delivery"}, 404
        return update_del

    update_delivery_response = update_delivery(request)

    if update_delivery_response.status_code == 200:
        return {"msg": "succesfull update"}
