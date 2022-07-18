import time
import json
import psutil
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

connection_string = 'HostName=msaunby.azure-devices.net;DeviceId=experimental-sensor;SharedAccessKey=25DxrXZaB9Q4eyOP22OB2R3QcGbdzKHelvKp1dWgZGs='
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')


def handle_method_request(request):
    print("Direct method received - ", request.name)
    
    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)


device_client.on_method_request_received = handle_method_request


def loop_body():
    temperature = 18
    print("Temperature:", temperature)

    data = psutil.sensors_temperatures()
    for x in data:
        print(x)
        for d in data[x]:
            print(d.current)

    message = Message(json.dumps({'temperature': temperature}))
    device_client.send_message(message)

    time.sleep(10)


while True:
    loop_body()