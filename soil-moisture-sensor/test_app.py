from unittest.mock import MagicMock, patch, mock_open

from app_class import SoilMoistureMonitor, connect, main


@patch('app_class.MethodResponse')
def test_handle_request(mock_method_response):
    mock_device_client = MagicMock()
    mock_adc = MagicMock()
    mock_relay = MagicMock()
    mock_request = MagicMock()
    mock_request.name = 'relay_on'
    mock_soil_moisture_monitor = SoilMoistureMonitor(adc=mock_adc, device_client=mock_device_client, relay=mock_relay)
    mock_soil_moisture_monitor.handle_request(request=mock_request)
    mock_method_response.create_from_method_request.assert_called_once_with(mock_request, 200)
    mock_device_client.send_method_response.assert_called_once_with(
        mock_method_response.create_from_method_request.return_value
    )
    mock_relay.on.assert_called_once()

    mock_request.name = 'relay_off'
    mock_soil_moisture_monitor.handle_request(request=mock_request)
    mock_relay.off.assert_called_once()


@patch('app_class.json')
@patch('app_class.Message')
def test_get_reading(mock_message, mock_json):
    mock_device_client = MagicMock()
    mock_adc = MagicMock()
    mock_relay = MagicMock()
    mock_soil_moisture_monitor = SoilMoistureMonitor(adc=mock_adc, device_client=mock_device_client, relay=mock_relay)
    mock_soil_moisture_monitor.get_reading()
    mock_adc.read.assert_called_once_with(0)
    mock_message.assert_called_once_with(mock_json.dumps({'soil_moisture': mock_adc.read.return_value}))
    mock_device_client.send_message.assert_called_once_with(mock_message.return_value)


@patch('app_class.IoTHubDeviceClient')
def test_connect(mock_client):
    mock_device_client = MagicMock()
    mock_adc = MagicMock()
    mock_relay = MagicMock()
    mock_client.create_from_connection_string.return_value = mock_device_client
    return_value = connect('test_value')
    mock_client.create_from_connection_string.assert_called_once_with('test_value')
    mock_device_client.connect.assert_called_once()
    assert return_value == mock_device_client


@patch('os.getenv')
@patch('app_class.connect')
@patch('app_class.take_readings')
@patch('app_class.SoilMoistureMonitor')
@patch('app_class.GroveRelay')
@patch('app_class.ADC')
def test_main(mock_adc, mock_grove_relay, mock_soil_moisture_monitor, mock_take_readings, mock_connect, mock_getenv):
    mock_getenv.return_value = 'test_connection_string'
    mock_device_client = MagicMock()
    mock_connect.return_value = mock_device_client
    main()
    mock_adc.assert_called_once()
    mock_grove_relay.assert_called_once_with(5)
    mock_connect.assert_called_once_with(connection_string='test_connection_string')
    mock_soil_moisture_monitor.assert_called_once_with(adc=mock_adc.return_value, relay=mock_grove_relay.return_value, device_client=mock_device_client)
