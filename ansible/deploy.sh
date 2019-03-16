#!/usr/bin/env bash
set -e

# Loading parameters from the local file
source parameters.sh

# Update hosts file from provided parameters
echo ${TARGET_DEVICE} > deployment-hosts

# Run the playbook
ansible-playbook -i deployment-hosts -u pi -v --ask-pass \
  --extra-vars "target_device=${TARGET_DEVICE} target_hostname=${TARGET_HOSTNAME} iot_greengrass_endpoint=${IOT_GREENGRASS_ENDPOINT} iot_data_endpoint=${IOT_DATA_ENDPOINT} iot_thing_arn=${IOT_THING_ARN}" \
  installation.yml