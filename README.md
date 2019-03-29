# home-energy-monitor
Power and Heat ingestion to AWS Cloud (using RPi and Ardiuno)



# Deploying Greengrass
- Setup a Greengrass group using the web interface
- Make a ZIP of the certificates according to the instructions in `ansible\certificates`
- Copy `ansible\parameters-example.sh` to `ansible\parameters.sh` and fill out the parameters. This information can be found in the generated `config.json` when creating the greengrass device via the console.
- Run the `deploy.sh`


# Temperature Monitor

# Power Monitor
`sudo apt-get install libbluetooth-dev`