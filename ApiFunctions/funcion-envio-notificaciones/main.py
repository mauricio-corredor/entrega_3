import os
import json
import requests

url_api_envio_notificaciones = os.environ.get('URL_API_ENVIO_NOTIFICACIONES', '')


def funcion_envio_notificaciones(datos):    
    print("Consumidor de Dispositivos para enviar notificaciones")
    print(url_api_envio_notificaciones)
    data = datos.get_json(force=True)
    print(data)
    if data == None:
        return "No se recibe información", 400
    try:
        print(url_api_envio_notificaciones)
        for device in data:
            pjson = json.dumps({"device-id": device['uuid'], "template-id": "", "extras": {} })
            print(pjson)
            envio_notificaciones = requests.post(url_api_envio_notificaciones, json = pjson)  
            print(envio_notificaciones)

        return "Notificaciones enviadas", 200
    except:
        return "Pago No actualizado", 404