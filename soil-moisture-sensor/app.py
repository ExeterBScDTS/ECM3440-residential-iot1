from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from modules.AzureIoTClient import AzureIoTClient

connection_string = 'HostName=anyaiothub.azure-devices.net;DeviceId=soil-moisture-sensor;SharedAccessKey=QRoksSHbOVbgt0BHz+xJdyzrMqsq1ht8n/Y8pif8mvs='

adc = ADC()
relay = GroveRelay(5)

def handle_method_request(request):
    print("Direct method received - ", request.name)
    
    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_request

if __name__ == '__main__':
    while True:
        soil_moisture = adc.read(0)
        print("Soil moisture:", soil_moisture)

        message = Message(json.dumps({ 'soil_moisture': soil_moisture }))
        device_client.send_message(message)

        time.sleep(10)

