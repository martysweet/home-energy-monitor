import os
import time
import json
import subprocess

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
sensors = {"top": "28-01142fed9cbf", "middle": "28-01143019315f", "bottom": "28-02131ab8bdaa"}
# TODO: Make sensors a deployment string for reusability


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


def lambda_handler(event, context):
    pass

# TODO: Make an envvar
topic = "/heating/temp"

while True:

    output = {}

    for key in sensors:
        output[key] = read_temp(sensors[key])

    messageJson = json.dumps(output)

    try:
        # TODO: Send message using greengrass
        pass
    except:
        print("Could not send message")

    time.sleep(60)
