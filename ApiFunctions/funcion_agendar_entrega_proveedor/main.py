from logging import exception
from google.cloud import tasks_v2
import requests
import os
import json

location_id = os.environ.get('LOCATION_ID', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function_consumidor = os.environ.get('URL_FUNCTION_CONSUMIDOR', '')
url_api_envio_agendar = os.environ.get('URL_API_ENVIO_AGENDAR', '')

client = tasks_v2.CloudTasksClient()

def funcion_agendar_entrega_proveedor(event):
    data = event['data']
    print(data)
    if data == None:
        return "No se recibe información", 400
    try:
        envio_agendar_response = requests.post(url_api_envio_agendar, json = {"direccion-origen": "direccion-origen","direccion-destino": "direccion-destino"})  
        if envio_agendar_response.status_code != 200:     
            return "Pedido No actualizado", envio_agendar_response.status_code

        print("Inicia Productor")
        parent = client.queue_path(projec_id, location_id, queue_id)
        task = {
            "http_request": {  
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url_function_consumidor,
                "headers": {
                    "Content-type": "application/json"
                },
                'body':json.dumps({'id':envio_agendar_response.json()['id'],'sellerId':data['sellerId'], 'userId': data['userId'], 'orderId':data['orderId'], 'estado':data['estado'], 'pickupDate':data['pickupDate'], 'deliveryDate':data['deliveryDate']}).encode()
            }
        }
        response = client.create_task(parent= parent, task= task)

        return {
            'message': 'Se crea la tarea Cola de entregas de manera exitosa',
            'name': response.name,
            'http_request': {
                'url' : response.http_request.url,
                'http_method' : str(response.http_request.http_method)
            }
        }    
        
    except Exception as e:
        print("No se agendó la entrega")
        print(e)
        return e, 404

# gcloud functions deploy funcion-entrega3-agendar-entrega-proveedor --entry-point funcion_agendar_entrega_proveedor --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --service-account "misw-entrega3-atormentados@entrega3-343303.iam.gserviceaccount.com" --set-env-vars QUEUE_ID=cola-entregas,LOCATION_ID=us-central1,PROJECT_ID=entrega3-343303,URL_FUNCTION_CONSUMIDOR=https://us-central1-entrega3-343303.cloudfunctions.net/funcion-entrega3-crear-agenda,URL_API_DISPOSITIVOS=https://gwintegraciones-baqkkpep.uc.gateway.dev/v1/envio/agendar