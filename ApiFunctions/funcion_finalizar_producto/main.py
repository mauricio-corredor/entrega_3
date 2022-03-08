from google.cloud import tasks_v2
import os
import json

location_id = os.environ.get('LOCATION_ID', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function = os.environ.get('URL_FUNCTION', '')

client = tasks_v2.CloudTasksClient()

def funcion_finalizar_producto(request):
    data = request.get_json(force=True)
    print(data)
    if data == None: 
        return "No se recibe información", 400

    parent = client.queue_path(projec_id, location_id, queue_id)

    task = {
        "http_request": {  
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url_function,
            "headers": {
                "Content-type": "application/json"
            },
            'body':json.dumps({'orderId':data['orderId'], 'estado':data['estado'], 'pickupDate':data['pickupDate'], 'deliveryDate':data['deliveryDate']}).encode()            
        }
    }
    response = client.create_task(parent= parent, task= task)
    
    return {
        'message': 'Se crea la tarea de manera exitosa',
        'name': response.name,
        'http_request': {
            'url' : response.http_request.url,
            'http_method' : str(response.http_request.http_method)
        }
    }

#gcloud functions deploy funcion-entrega3-finalizar-producto --entry-point funcion_finalizar_producto --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --service-account "misw-entrega3-atormentados@entrega3-343303.iam.gserviceaccount.com" --set-env-vars QUEUE_ID=cola-finalizar-producto,LOCATION_ID=us-central1,PROJECT_ID=entrega3-343303,URL_FUNCTION=https://us-central1-entrega3-343303.cloudfunctions.net/funcion-entrega3-actualizar-pedido-finalizado