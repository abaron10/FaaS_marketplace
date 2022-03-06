from google.cloud import tasks_v2
import os

location_id = os.environ.get('LOCATION_ID', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function = os.environ.get('URL_FUNCTION', '')
client = tasks_v2.CloudTasksClient()

def producir(request):
    parent = client.queue_path(projec_id, location_id, queue_id)
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url_function,
            "headers": {
                "Content-type": "application/json"
            },
            "body": request.data,
        }
    }
    response = client.create_task(request={"parent": parent, "task": task})
    return {
        'message': 'Se crea la tarea de manera exitosa',
        'name': response.name,
        'http_request': {
            'url' : response.http_request.url,
            'http_method' : str(response.http_request.http_method)
        }
    }
