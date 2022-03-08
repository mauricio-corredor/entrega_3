from google.cloud import pubsub_v1
import requests
import os
import json


url_api_crear_agenda = os.environ.get('URL_API_CREAR_AGENDA', '')
topic_path = os.environ.get('TOPIC_PATH','')


publisher = pubsub_v1.PublisherClient()

def funcion_crear_agenda(datos):
    data = datos.get_json(force=True)
    print(data)
    if data == None:
        return "No se recibe información", 400
    try:
        url = f"{url_api_crear_agenda}/{data['sellerId']}"
        orderId = data['orderId']
        crear_agenda = requests.post(url, json = {"uuid": orderId })  
        if crear_agenda.status_code != 201:     
            return "No se creó la agenda", crear_agenda.status_code

        print("Inicia Publicador")                
        mensaje = json.dumps({'sellerId':data['sellerId'], 'userId': data['userId'], 'orderId':data['orderId'], 'estado':data['estado'], 'pickupDate':data['pickupDate'], 'deliveryDate':data['deliveryDate']}).encode('utf-8')
        publish_future = publisher.publish(topic_path, data=mensaje)
        publish_future.result() 
        return 'Se envia el mensaje a TOPIC'
        
    except Exception as e:
        print('Error al momento de publicar')
        print(e)
        return e

# gcloud functions deploy funcion-entrega3-publicador-agenda --entry-point funcion_crear_agenda --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars TOPIC=agenda,URL_API_CREAR_AGENDA=http://34.111.176.85/agenda/sellers