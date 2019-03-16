#!/usr/bin/env bash

# Specifies what you want to call the RPI to distinguish it
# on your network.
# > target_hostname
TARGET_HOSTNAME="HomeEnergyMonitor"

# IP/Hostname which the Ansible playbook is run against.
# > target_device
TARGET_DEVICE="192.168.1.2"

# The Thing ARN of the Greengrass Core you are deploying.
# > iot_thing_arn
IOT_THING_ARN="arn:aws:iot:eu-west-1:00000000000:thing/HomeEnergyMonitor"

# Your custom IOT endpoint for pub/sub communication.
# > iot_data_endpoint
IOT_DATA_ENDPOINT="abcdefg-ats.iot.eu-west-1.amazonaws.com"

# The greengrass endpoint for communication.
# > iot_greengrass_endpoint
IOT_GREENGRASS_ENDPOINT="greengrass-ats.iot.eu-west-1.amazonaws.com"