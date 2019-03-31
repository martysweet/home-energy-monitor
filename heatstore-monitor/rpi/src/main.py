import os
import time
import json
import subprocess
import greengrasssdk

gg_client = greengrasssdk.client('iot-data')

base_dir = '/sys/bus/w1/devices/'

# Environmental Variables
try:
    poll_delay = int(os.environ['POLL_DELAY'])
    sensors = {
        "top":      os.environ['SENSOR_TOP_ID'],
        "middle":   os.environ['SENSOR_MIDDLE_ID'],
        "bottom":   os.environ['SENSOR_BOTTOM_ID']
    }
except Exception as e:
    print("Failed parsing environmental variables: {}".format(e))
    raise

# CloudWatch Configuration
cw_payload_field_mappings = {
    'top':      'Top',
    'middle':   'Middle',
    'bottom':   'Bottom'
}

cw_namespace = 'House/Monitoring/Heatstore'
cw_topic = 'cloudwatch/metric/put'


def lambda_handler(event, context):
    print("Lambda handler called.")
    return True


def read_temp_raw(device_file):
    print("Attempting to read: {}".format(device_file))
    catdata = subprocess.Popen(['/bin/cat', device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines


def read_temp(sensor_id):
    lines = read_temp_raw(base_dir + sensor_id + "/w1_slave")
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(base_dir + sensor_id + "/w1_slave")
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def send_metrics_from_dict(d):
    for f in cw_payload_field_mappings:
        val = d.get(f, None)
        if val is not None:
            payload = {
                "request": {
                    "namespace": cw_namespace,
                    "metricData": {
                        "metricName": "Temperature",
                        "dimensions": [
                            {
                                'name': 'Device',
                                'value': 'Heatstore'
                            },
                            {
                                'name': 'Probe',
                                'value': cw_payload_field_mappings[f]
                            },
                        ],
                        "value": float(val),
                        "timestamp": time.time()
                    }
                }
            }
            # Publish to connector
            gg_client.publish(topic=cw_topic, payload=json.dumps(payload))


def read_sensors():
    while True:

        # Read top/middle/bottom sensors
        output = {}
        for key in sensors:
            output[key] = read_temp(sensors[key])

        # Send the metrics off, for top/middle/bottom
        send_metrics_from_dict(output)

        # Sleep until we try again
        time.sleep(poll_delay)  # TODO: This is majorly affected by drift, caused by the
                                # TODO: delay it takes to read_temp. Need to use a scheduler here.

# Run forever
while True:
    try:
        read_sensors()
    except Exception as e:
        print("Failed reading sensors, will retry: {}".format(e))