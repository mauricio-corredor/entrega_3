from flask import jsonify
def enviodelosalpes(request):
    data = request.get_json(force=True)
    if data == None: #Si el objeto está vácio se retorna error
        return "No se recibe información", 400
    print("id:" + data['id'])
    print("timestamp:" + data['timestamp'])
    print("operationId:" + data['operationId'])
    print("pickupDate:" + data['pickupDate'])
    print("deliveryDate:" + data['deliveryDate'])
    print("lat:" + data['lat'])
    print("lng:" + data['lng'])
    return "OK"




from google.cloud import tasks_v2
import os
import json

location_id = os.environ.get('LOCATION_ID', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function = os.environ.get('URL_FUNCTION', '')

client = tasks_v2.CloudTasksClient()

def pagosdelosalpes(request):
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
            'body':json.dumps({'payment_uuid':data['id'], 'estado':data['estado']}).encode()
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