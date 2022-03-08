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

def funcion_actualizar_pedido_finalizado(datos):
    data = datos.get_json(force=True)
    print(data)
    if data == None:
        return "No se recibe información", 400
    try:
        url = f"{url_api_actualizar_pedido}/{data['orderId']}"
        estado = data['estado']
        actualizar_pedido_response = requests.post(url, json = {"state": estado })  
        if actualizar_pedido_response.status_code != 200:     
            return "Pedido No actualizado", actualizar_pedido_response.status_code

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
                'body':json.dumps({'sellerId':actualizar_pedido_response.json()['sellerId'], 'userId': actualizar_pedido_response.json()['userId'], 'orderId':data['orderId'], 'estado':data['estado'], 'pickupDate':data['pickupDate'], 'deliveryDate':data['deliveryDate']}).encode()
            }
        }
        response = client.create_task(parent= parent, task= task)

        return {
            'message': 'Se crea la tarea Crear Agenda de manera exitosa',
            'name': response.name,
            'http_request': {
                'url' : response.http_request.url,
                'http_method' : str(response.http_request.http_method)
            }
        }    
        
    except:
        return "Pedido No actualizado", 404

# gcloud functions deploy funcion-entrega3-actualizar-pedido-finalizado --entry-point funcion_actualizar_pedido_finalizado --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --service-account "misw-entrega3-atormentados@entrega3-343303.iam.gserviceaccount.com" --set-env-vars QUEUE_ID=cola-crear-agenda,LOCATION_ID=us-central1,PROJECT_ID=entrega3-343303,URL_FUNCTION_CONSUMIDOR=https://us-central1-entrega3-343303.cloudfunctions.net/funcion-entrega3-crear-agenda,URL_API_DISPOSITIVOS=http://34.111.176.85/orders/internal