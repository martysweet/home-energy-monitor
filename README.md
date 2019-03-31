# home-energy-monitor
This project uses a verity of sensors and a Raspberry Pi 3B+ to ingest the data
using GreenGrass into CloudWatch using the Greengrass/CloudWatch connector for graphing. 
The entire stack and deployment is code based, using Ansible and CloudFormation.
See below for more details on each component.

# Components
## Power Monitor
The power monitor is based off an Ardiuno Nano and a stripboard based from Open Energy Monitors Buffered Voltage Bias
design. The code is included within the `power-monitor\ardiuno` directory and uses the `EmonLib` library for calculate the real power usage.
This code can be compiled using https://create.arduino.cc. The data is then sent over bluetooth (using a HC-05) to the RPi, where it is ingested
via the CloudWatch metric connector.


Buffered Voltage Schematic: https://learn.openenergymonitor.org/electricity-monitoring/ctac/acac-buffered-voltage-bias


## Heatstore Monitor
The RPi is connected to 3 one-wire sensors, which are each located within temperature probe locations
within a Heat Store water unit. The sensors are polled periodically, before the metrics are sent to the 
CloudWatch metric connector.

`dtoverlay=w1-gpio` was added to the bottom of /boot/config.txt (TODO: Implement in Ansible). 

## Water Monitor
The water monitor runs the on RPi and calls a remote Modbus server (Crouzet EM4), which keeps
a counter based on a pulse water meter, where each pulse represents 10 Litres of water 
usage. The Water Monitor calculates the difference between the current and previous
reading before posting the difference to CloudWatch metrics.

## Heating Monitor
This code interfaces with the Heatmiser NeoHub API to collect data regarding room temperature, and if the 
heating is currently active in a specific zone. Publishing metrics to the CloudWatch connector.
Inspired from https://github.com/RJ/heatmiser-neohub.py, this implemention is simplified just to pull out each device's basic information.

# Getting Started
## Step 1 - Deploying CloudFormation
1. Create a certificate in the AWS IoT console and note the Principal ARN, download the certificates.
2. Copy `env-example.sh` to `env.sh` and populate the options.
3. Copy `template-parameters-example.json` to `template-parameters.json` and populate the parameters.
4. Run the `deploy.sh` script to deploy the stack to your environment.
5. Once the stack has been created, navigate to the console and make the Power Monitor Lambda function run in 'NoContainer'. This is to overcome a current CloudFormation bug with Greengrass.
6. Deploy the Greengrass group, this will then be downloaded automatically when the RPi is setup.

## Step 2 - Deploying Ansible
1. Ensure you have downloaded the certificates and deployed the Greengrass.
2. Put the `random-certificate.pem.crt` and `random-private.pem.key` certificates in the `ansible\certificates` directory.
3. Copy the `ansible\parameters-example.sh` to `ansible\parameters.sh` and populate the options. IOT_THING_ARN and IOT_DATA_ENDPOINT can be found from the IoT console, IOT_CERT_ID is the random ID of the downloaded certificates.
4. cd into `ansible`
5. Run `deploy.sh` to deploy the ansible configuration to the RPi, this will configure Greengrass and it's dependencies and copy your certificates 