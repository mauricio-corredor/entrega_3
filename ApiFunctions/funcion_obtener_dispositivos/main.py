from google.cloud import tasks_v2
import requests
import os
import json

location_id = os.environ.get('LOCATION_ID', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function_consumidor = os.environ.get('URL_FUNCTION_CONSUMIDOR', '')
url_api_dispositivos = os.environ.get('URL_API_DISPOSITIVOS', '')

client = tasks_v2.CloudTasksClient()

def funcion_obtener_dispositivos(datos):
    #location_id="us-central1"
    #projec_id = "entrega3-343303"
    #queue_id = "cola-envio-notificaciones"
    print("location_id: " + location_id)
    print("project_id: " + projec_id)
    print("queue_id: " + queue_id)

    data = datos.get_json(force=True)
    print(data)
    if data == None:
        return "No se recibe información", 400
    try:
        #url_api_dispositivos = "http://34.111.176.85/devices/user"
        print("URL: " + url_api_dispositivos)

        url = f"{url_api_dispositivos}/{data['userId']}"
        print(url)            
        
        obtener_dispositivos_response = requests.get(url)  
        print(obtener_dispositivos_response.json())
        print("DUMPS")
        print(json.dumps(obtener_dispositivos_response.json()).encode())
        if obtener_dispositivos_response.status_code != 200:
            return "No se obtuvieron dispositivos", obtener_dispositivos_response.status_code            

        print("Inicia Productor")
        #url_function_consumidor = "https://us-central1-entrega3-343303.cloudfunctions.net/funcion-entrega3-envio-notificaciones"
        print(url_function_consumidor)
        parent = client.queue_path(projec_id, location_id, queue_id)
        print(parent)
        task = {
            "http_request": {  
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url_function_consumidor,
                "headers": {
                    "Content-type": "application/json"
                },
                'body': json.dumps(obtener_dispositivos_response.json()).encode()
            }
        }
        print("Imprime task")
        print(task)
        print("Crear Tarea en cola")
        response = client.create_task(parent= parent, task= task)
        print("Se Creó Tarea en cola")
        return {
            'message': 'Se crea la tarea Envio notificaciones de manera exitosa',
            'name': response.name,
            'http_request': {
                'url' : response.http_request.url,
                'http_method' : str(response.http_request.http_method)
            }
        }
        
    except:
        return "Error al obtener dispositivos", 404