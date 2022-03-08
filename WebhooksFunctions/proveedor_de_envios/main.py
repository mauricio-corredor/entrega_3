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
