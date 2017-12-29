#PyASEAG
Python wrapper for ASEAG live monitor api (URA) including a Mattermost integration based on Flask.

##Features:
* Simple to use wrapper for most important ASEAG api functions
* Fuzzy matching of queried bus stop name with all available bus stops
* Predicted arrivals of buses are formatted as table
* Ready to use integration for ;attermost (BusBot)

## Requirements
* Linux (because of Gunicorn)
* Python 3 (tested on 3.5.3)
* Further dependencies are specified in requirements.txt

## Usage
Most of the parameters can be changed in the `config.py`. If you would like to use the Mattermost integration, you have
to add the url and token of your previously created Mattermost /slash integration. You can run the integration by
running `run_mattermost.sh`

## License
PyASEAG is available under the MIT license.