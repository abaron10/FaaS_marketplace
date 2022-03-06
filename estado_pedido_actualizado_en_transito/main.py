from variables import ORDERS_SERVER, NOTIFICATIONS_SERVER
import requests
from datetime import datetime, timedelta


def actualizacion_estado_pedido_en_transito(request=None):
    order_id = request.get_json()['orderId']
    url = f'http://{ORDERS_SERVER}/orders/internal/{order_id}'
    update_delivery = requests.post(url, data={'state': 'EN_TRANSITO'})

    if update_delivery.status_code != 200:
        return {'msg': 'error while updating delivery'}, 404

    url_notifications = f'https://{NOTIFICATIONS_SERVER}/funcion-notificaciones-producir'

    date_user = datetime.now() + timedelta(days=4)
    notification_body_user = {
        'notificacion': f'La fecha de entrega de su pedido con id {order_id} es: {date_user}',
        'type': 1,
        'order_id': order_id
    }

    date_seller = datetime.now() + timedelta(days=1)
    notification_body_seller = {
        'notificacion': f'La fecha de recolección del pedido con id {order_id} es: {date_seller}',
        'type': 0,
        'order_id': order_id
    }

    send_user_notification = requests.post(url_notifications, data=notification_body_user)
    send_seller_notification = requests.post(url_notifications, data=notification_body_seller)

    if send_user_notification.status_code != 200 or send_seller_notification.status_code != 200:
        return {'msg': 'error while notificating user or seller'}, 404
    else:
        return {'msg': 'successful update and notification'}
