import bluetooth
import time
import json
import greengrasssdk
import os

gg_client = greengrasssdk.client('iot-data')

# Target BT Address
try:
    target_bt_addr = os.environ['BT_ADDRESS']
except Exception as e:
    print("Failed parsing environmental variables: {}".format(e))

# CloudWatch Configuration
cw_payload_field_mappings = {
    'i1':   'Grid',
    'i2':   'Solar',
    'i3':   'WaterImmersion',
    'i4':   'ASHP',
    'i5':   'BufferImmersion',
  #  'Vrms': 'Voltage'
}

cw_namespace = 'House/Monitoring/Electricity'
cw_topic = 'cloudwatch/metric/put'

# Debug Counters
mess_buff_count = 0                 # When a bluetooth buffer is filled
mess_succ_count = 0                 # When a message is successfully parsed as JSON
mess_invalid_count = 0              # When a message is invalid JSON
blueth_conn_attempts = 0            # For each time a Bluetooth connection is attempted


def lambda_handler(event, context):
    print("Lambda Handler Called. "
          "Buffer Receives: {}. "
          "Successful Messages: {}."
          "Invalid Messages: {}."
          "Bluetooth disconnects: {}.".format(mess_buff_count,
                                              mess_succ_count,
                                              mess_invalid_count,
                                              blueth_conn_attempts))
    return True


def handle_mesg(msg):
    global mess_invalid_count, mess_succ_count

    # Check this is valid JSON
    try:
        ard_resp = json.loads(msg)
    except Exception:
        print("Invalid JSON - Possibly faulty transmission.")
        mess_invalid_count += 1
        return

    # Send to IOT Topic
    mess_succ_count += 1
    print("Sending to IOT: {}".format(msg))

    # For every configured field, publish the metric directly
    send_metrics_from_dict(ard_resp)


def send_metrics_from_dict(d):
    for f in cw_payload_field_mappings:
        val = d.get(f, None)
        if val is not None:
            payload = {
                "request": {
                    "namespace": cw_namespace,
                    "metricData": {
                        "metricName": "Power",
                        "dimensions": [
                            {
                                'name': 'Device',
                                'value': 'PowerMonitor'
                            },
                            {
                                'name': 'Circuit',
                                'value': cw_payload_field_mappings[f]
                            }
                        ],
                        "value": float(val),
                        "timestamp": time.time()
                    }
                }
            }
            # Publish to connector
            gg_client.publish(topic=cw_topic, payload=json.dumps(payload))

    # Send voltage
    payload = {
        "request": {
            "namespace": cw_namespace,
            "metricData": {
                "metricName": "Voltage",
                "dimensions": [
                    {
                        'name': 'Device',
                        'value': 'PowerMonitor'
                    },
                    {
                        'name': 'Circuit',
                        'value': cw_payload_field_mappings['i1']
                    }
                ],
                "value": float(d.get('Vrms')),
                "timestamp": time.time()
            }
        }
    }

    # Publish to connector
    gg_client.publish(topic=cw_topic, payload=json.dumps(payload))


def connect_bluetooth():
    global mess_buff_count
    # Connection Details
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((target_bt_addr, port))
    print('Connected')

    try:
        buffer = ''
        while True:
            data = sock.recv(4096)
            buffer = buffer + data
            mess_buff_count += 1
            if len(buffer) > 2:
                if buffer[-2:] == "\r\n":
                    handle_mesg(buffer)
                    buffer = ''
            # Sleep to allow the Lambda handler to be invoked if needed
            time.sleep(0.1)
    finally:
        sock.close()


while True:
    blueth_conn_attempts += 1
    try:
        connect_bluetooth()
    except Exception as e:
        print("Exception, continuing: {}".format(e))


