import json
import requests
import ast
import env_vars as env

# Type 0 - Vendedor
# Type 1 - Comprador
def consumir(request):
    data = request.data
    string_data = data.decode('utf8')
    dict_data = ast.literal_eval(string_data)

    # TODO: El servicio falla algunas veces
    def get_device(order_id, is_user):
        url = f'{env.get_base_url()}/orders/{order_id}'
        update_del = requests.get(url)
        if update_del.status_code != 200:
            return {"msg":"error while updating delivery"}

        response = update_del.json()
        user_id = response["userId"] if is_user else response["sellerId"]
        url = f'{env.get_base_url()}/devices/user/{user_id}'
        device_id = requests.get(url)
        if device_id.status_code != 200:
            return {"msg":"error while updating delivery"}
        return device_id.json()

    device_data = get_device(
        dict_data['order_id'], dict_data['order_id'] == 1
    )
    notification = {
        "device-id": device_data[0]["uuid"],
        "template-id": dict_data['notificacion'],
        "extras": {}
    }

    notification_response = requests.post(
        'https://gwintegraciones-baqkkpep.uc.gateway.dev/v1/notificar/device',
        json=notification
    )

    return notification_response.json()
