from google.cloud import tasks_v2
import requests
import os
import json

location_id = os.environ.get('LOCATION_ID', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function_consumidor = os.environ.get('URL_FUNCTION_CONSUMIDOR', '')
url_api_actualizar_pedido = os.environ.get('URL_API_ACTUALIZAR_PEDIDO', '')

client = tasks_v2.CloudTasksClient()


def funcion_actualizar_pedido(datos):
    print(location_id)
    print(projec_id)
    print(queue_id)
    print(url_function_consumidor)
    print(url_api_actualizar_pedido)

    data = datos.get_json(force=True)
    print(data)
    if data == None:
        return "No se recibe información", 400
    try:
        url = f"{url_api_actualizar_pedido}/{data['orderId']}"
        estado = data['estado']
        actualizar_pedido_response = requests.post(url, json = {"state": estado })  
        print(actualizar_pedido_response.json())
        print(actualizar_pedido_response.status_code)
        if actualizar_pedido_response.status_code != 200:     
            return "Pedido No actualizado", actualizar_pedido_response.status_code
        
        if estado != 'ACEPTADO':
            return "Estado de pedido actualizado", 200

        print("Inicia Productor")
        print(actualizar_pedido_response.json()['sellerId'])
        parent = client.queue_path(projec_id, location_id, queue_id)
        task = {
            "http_request": {  
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url_function_consumidor,
                "headers": {
                    "Content-type": "application/json"
                },
                'body':json.dumps({'userId':actualizar_pedido_response.json()['sellerId']}).encode()
            }
        }
        response = client.create_task(parent= parent, task= task)

        return {
            'message': 'Se crea la tarea Obtener Dispositivos de manera exitosa',
            'name': response.name,
            'http_request': {
                'url' : response.http_request.url,
                'http_method' : str(response.http_request.http_method)
            }
        }    
        
    except:
        return "Pedido No actualizado", 404