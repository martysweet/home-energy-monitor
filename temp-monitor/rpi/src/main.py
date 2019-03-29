import os
import time
import json
import subprocess
import greengrasssdk

gg_client = greengrasssdk.client('iot-data')

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

# TODO: Make sensors a deployment string for reusability
poll_delay = os.environ['POLL_DELAY']
sensors = {
    "top":      os.environ['SENSOR_TOP_ID'],
    "middle":   os.environ['SENSOR_MIDDLE_ID'],
    "bottom":   os.environ['SENSOR_BOTTOM_ID']
}

# CloudWatch Configuration
cw_payload_field_mappings = {
    'top':      'HeatstoreTop',
    'middle':   'HeatstoreMiddle',
    'bottom':   'HeatstoreBottom'
}

cw_dimensions = [
    {
        'Name': 'Device',
        'Value': 'Heatstore'
    },
]

cw_namespace = 'House/Monitoring'
cw_topic = 'cloudwatch/metric/put'


def lambda_handler(event, context):
    print("Lambda handler called.")
    return True


def read_temp_raw(device_file):
    catdata = subprocess.Popen(['cat', device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                        "metricName": cw_payload_field_mappings[f],
                        "dimensions": cw_dimensions,
                        "value": val,
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
        time.sleep(poll_delay)

# Run forever
while True:
    try:
        read_sensors()
    except Exception as e:
        print("Failed reading sensors, will retry: {}".format(e))