import bluetooth
import time

def lambda_handler(event, context):
    pass


# Connection Details
port = 1
target_addr = "98:D3:31:F5:C0:FA"
# sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM)

print(bluetooth.find_service(address='00:13:EF:C0:02:1E'))