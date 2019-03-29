import bluetooth
import time
import json


mess_buff_count = 0         # When a bluetooth buffer is filled
mess_succ_count = 0         # When a message is successfully parsed as JSON
mess_invalid_count = 0      # When a message is invalid JSON
blueth_conn_attempts = 0    # For each time a Bluetooth connection is attempted


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
        json.loads(msg)
    except Exception:
        print("Invalid JSON - Possibly faulty transmission.")
        mess_invalid_count += 1
        return

    # Send to IOT Topic
    mess_succ_count += 1
    print("Sending to IOT: {}".format(msg))


def connect_bluetooth():
    global mess_buff_count
    # Connection Details
    target_addr = "98:D3:31:F5:C0:FA" # TODO ENVVAR

    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((target_addr, port))
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


