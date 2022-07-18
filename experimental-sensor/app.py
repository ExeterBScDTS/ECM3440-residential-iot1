import time
import json
import psutil
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from azure.iot.device.exceptions import ConnectionFailedError

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
    data = psutil.sensors_temperatures()
    temperature = data['pch_skylake'][0].current
    print("Temperature:", temperature)

    message = Message(json.dumps(
        {'kind': 'temperature', 'value': temperature}
    ))
    try:
        device_client.send_message(message)
    except ConnectionFailedError:
        print("Failed to send message")

    #time.sleep(5*60)
    time.sleep(2 * 60)


while True:
    loop_body()
