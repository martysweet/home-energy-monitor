from pyModbusTCP.client import ModbusClient
import time
import json
import greengrasssdk
import os

gg_client = greengrasssdk.client('iot-data')

try:
    host = os.environ['MODBUS_HOST']
    poll_delay = int(os.environ['POLL_DELAY'])
    k = int(os.environ['WATER_METER_K'])     # Unit of the pulse meter, i.e. K=10L (Litres)
except Exception as e:
    print("Failed parsing environmental variables: {}".format(e))

# Cloudwatch Configuration
cw_namespace = 'House/Monitoring/Water'
cw_topic = 'cloudwatch/metric/put'


def lambda_handler(event, context):
    print("Lambda Handler Called.")
    return True


def read_values():
    c = ModbusClient(host=host, auto_open=True, auto_close=True)
    old_value = -1

    while True:

        new_value = int(c.read_holding_registers(43, 1)[0])
        print("New Value: {}".format(new_value))

        if old_value == -1:
            print("Setting old value to new value.")
            old_value = new_value   # Set the old_value so we don't do weird looping

        # Detect if the counter has been reset
        if new_value < old_value:
            print("Counter has been reset externally. Force set.")
            old_value = new_value

        print("Old: {}. New: {}.".format(old_value, new_value))
        diff = new_value - old_value
        old_value = new_value

        # Push to CloudWatch, even if the value is 0
        litres = diff * float(k)
        payload = {
            "request": {
                "namespace": cw_namespace,
                "metricData": {
                    "metricName": "UsageLitres",
                    "dimensions": [
                        {
                            'name': 'Device',
                            'value': 'WaterPulseMeter'
                        },
                        {
                            'name': 'Supply',
                            'value': 'Mains'
                        },
                    ],
                    "value": litres,
                    "timestamp": time.time()
                }
            }
        }
        # Publish to connector
        gg_client.publish(topic=cw_topic, payload=json.dumps(payload))

        time.sleep(poll_delay)


# Run, let the GG ENV, restart on failure
read_values()
