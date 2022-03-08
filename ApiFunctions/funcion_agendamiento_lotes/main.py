from google.cloud import tasks_v2
import requests
import os
import json
from google.cloud import datastore
from flask import jsonify

location_id = os.environ.get('LOCATION_ID', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function_consumidor = os.environ.get('URL_FUNCTION_CONSUMIDOR', '')
url_api_actualizar_pedido = os.environ.get('URL_API_ACTUALIZAR_PEDIDO', '')

client = tasks_v2.CloudTasksClient()
datastore_client = datastore.Client()
kind = "Agenda"


def funcion_agendar_lotes(datos):

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

        # Creación de un objeto para consumo de de la entidad a trabajar
        query = datastore_client.query(kind=kind)
        query.add_filter("estado","=",data['estado'])
        results = list(query.fetch())

        registros = jsonify(results)

        for registro in registros:

            print("Inicia Productor")            
            parent = client.queue_path(projec_id, location_id, queue_id)
            task = {
                "http_request": {  
                    "http_method": tasks_v2.HttpMethod.POST,
                    "url": url_function_consumidor,
                    "headers": {
                        "Content-type": "application/json"
                    },
                    'body':json.dumps({'id':registro['id'], 'operationId':'AGENDADO', 'pickupDate':registro['pickupDate'], 'deliveryDate':registro['deliveryDate']}).encode()
                }
            }
            response = client.create_task(parent= parent, task= task)

        return {
            'message': 'Se crea la tarea envios los alpes de manera exitosa',
            'name': response.name,
            'http_request': {
                'url' : response.http_request.url,
                'http_method' : str(response.http_request.http_method)
            }
        }    
        
    except:
        return "Pedido No actualizado", 404