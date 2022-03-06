from variables import SERVER, SERVER_THIRD_PARTIES
import requests


def actualizacion_estado_pedido_entregado(request=None):
    order_id = request.get_json()['orderId']
    url_orders = f'http://{SERVER}/orders/internal/{order_id}'
    update_delivery = requests.post(url_orders, data={'state': 'ENTREGADO'})

    if update_delivery.status_code != 200:
        return {'msg': 'error while updating delivery'}, 404

    external_id = request.get_json()['externalId']
    url_factura = f'https://{SERVER_THIRD_PARTIES}/factura/generar'

    data = {'external-id': external_id}
    headers = {'Content-type': 'application/json'}
    generar_factura = requests.post(url_factura, json=data, headers=headers)

    #TODO: Notificar al vendedor
    if generar_factura.status_code != 200:
        return {'msg': 'error while updating delivery'}, 404
    else:
        return {'msg': 'succesful update'}
