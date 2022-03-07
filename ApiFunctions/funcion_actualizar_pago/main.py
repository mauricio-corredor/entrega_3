from google.cloud import tasks_v2
import requests
import os
import json

location_id = os.environ.get('LOCATION_ID', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function_consumidor = os.environ.get('URL_FUNCTION_CONSUMIDOR', '')
url_api_actualizar_pago = os.environ.get('URL_API_ACTUALIZAR_PAGO', '')

client = tasks_v2.CloudTasksClient()

def funcion_actualizar_pago(datos):
    data = datos.get_json(force=True)
    print(data)
    if data == None:
        return "No se recibe información", 400
    try:
        url = f"{url_api_actualizar_pago}/{data['payment_uuid']}"
        actualizar_pago_response = requests.post(url, json = {"state": data['estado'] })  
        print(actualizar_pago_response.json())
        if actualizar_pago_response.status_code != 201:
            return "Pago No actualizado", actualizar_pago_response.status_code            
        
        print("Inicia Productor")
        print({'orderId':actualizar_pago_response.json()['orderId'], 'estado':actualizar_pago_response.json()['state']})
        parent = client.queue_path(projec_id, location_id, queue_id)
        task = {
            "http_request": {  
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url_function_consumidor,
                "headers": {
                    "Content-type": "application/json"
                },
                'body':json.dumps({'orderId':actualizar_pago_response.json()['orderId'], 'estado':actualizar_pago_response.json()['state']}).encode()
            }
        }
        response = client.create_task(parent= parent, task= task)

        return {
            'message': 'Se crea la tarea Actualizar pedido de manera exitosa',
            'name': response.name,
            'http_request': {
                'url' : response.http_request.url,
                'http_method' : str(response.http_request.http_method)
            }
        }
        
    except:
        return "Pago No actualizado", 404