from logging import exception
from google.cloud import tasks_v2
from google.cloud import datastore
from flask import jsonify
import requests
import os
import json


url_api_envio_agendar = os.environ.get('URL_API_ENVIO_AGENDAR', '')

client = tasks_v2.CloudTasksClient()
datastore_client = datastore.Client()
kind = "Agenda"


def funcion_agendar_entrega_proveedor(event):
    data = event['data']
    print(data)
    if data == None:
        return "No se recibe información", 400
    try:
        envio_agendar_response = requests.post(url_api_envio_agendar, json = {"direccion-origen": "direccion-origen","direccion-destino": "direccion-destino"})  
        if envio_agendar_response.status_code != 200:     
            return "No se agendó", envio_agendar_response.status_code

        print("Inicia Copia a BD")
        task_key = datastore_client.key(kind)
        nueva_agenda = datastore.Entity(key=task_key)
        nueva_agenda["id"] = envio_agendar_response.json()['id']
        nueva_agenda["sellerId"] = data['sellerId']
        nueva_agenda["userId"] = data['userId']
        nueva_agenda["orderId"] = data['orderId']
        nueva_agenda["estado"] = data['estado']
        nueva_agenda["pickupDate"] = data['pickupDate']
        nueva_agenda["deliveryDate"] = data['deliveryDate']

        datastore_client.put(nueva_agenda)


        return jsonify(nueva_agenda)
        
    except Exception as e:
        print("Error al registrar agenda")
        print(e)
        return e, 400

# gcloud functions deploy funcion-entrega3-agendar-entrega-proveedor --entry-point funcion_agendar_entrega_proveedor --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --service-account "misw-entrega3-atormentados@entrega3-343303.iam.gserviceaccount.com" --set-env-vars URL_API_DISPOSITIVOS=https://gwintegraciones-baqkkpep.uc.gateway.dev/v1/envio/agendar