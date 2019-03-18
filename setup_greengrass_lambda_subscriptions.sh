#!/usr/bin/env bash

# Deploy the functions
# TODO We need to provide envars here - perhaps use Python instead?
./gghelper lambda -pinned -d power-monitor/rpi/src -handler main.lambda_handler -name HEM-RPI-Power-Monitor \
            -role lambda_basic_execution -runtime python2.7 -p $AWS_PROFILE

./gghelper lambda -pinned -d temp-monitor/rpi/src -handler main.lambda_handler -name HEM-RPI-Temp-Monitor \
            -role lambda_basic_execution -runtime python2.7 -p $AWS_PROFILE

# Setup the allowed incoming messages
./gghelper createsub -source HEM-RPI-Power-Monitor -target cloud -subject "hem/power"
./gghelper createsub -source HEM-RPI-Temp-Monitor -target cloud -subject "hem/temp"

# Create the deployment
./gghelper createdeployment
