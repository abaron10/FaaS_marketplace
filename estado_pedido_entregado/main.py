from variables import SERVER, SERVER_THIRD_PARTIES, NOTIFICATIONS_SERVER
import requests
import time


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

    if generar_factura.status_code != 200:
        return {'msg': 'error while generating invoice'}, 404

    factura_id = generar_factura.json()['id']
    url_factura_get = f'https://{SERVER_THIRD_PARTIES}/factura/obtener/{factura_id}'
    obtener_factura = requests.get(url_factura_get)

    while obtener_factura.status_code != 200:
        time.sleep(1)
        obtener_factura = requests.get(url_factura_get)
        print(obtener_factura)

    url_notifications = f'https://{NOTIFICATIONS_SERVER}/funcion-notificaciones-producir'
    notification_body_seller = {
        'notificacion': f'Se generó una factura con id: {factura_id} para el pedido con id: {order_id}',
        'type': 0,
        'order_id': order_id
    }
    send_seller_notification = requests.post(url_notifications, data=notification_body_seller)

    if send_seller_notification.status_code != 200:
        return {'msg': 'error while notificating seller'}, 404
    else:
        return {'msg': 'successful update and notification'}
