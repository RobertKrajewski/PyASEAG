import requests
import json
from collections import namedtuple
from typing import List
import config

BusStop = namedtuple("BusStop", "name id lat long")
BusStopPrediction = namedtuple("BusStopPrediction", "stop_id line_name dest_name estimated_time")


def get_all_stops() -> List[BusStop]:
    """
    Calls the ASEAG api (URA) to get a list of all available bus stops.

    :return: A list of the named tuple BusStop containing the name, api id and the lat/long position of the stop.
    """
    payload = {"StopAlso": "true",
               "ReturnList": "StopPointName,StopID,Latitude,Longitude"}
    result = requests.get(config.base_url, params=payload)

    if result.status_code != 200:
        raise Exception("ASEAG api request returned status code %i" % result.status_code )

    # Read in all bus stops, line by line
    bus_stops = []
    for line in result.text.splitlines():
        line_list = json.loads(line)

        # Line contains bus stop, if first entry is a '0'. Also remove test bus stops names '.'
        if line_list[0] == 0 and line_list[1] != ".":
            bus_stops.append(BusStop(*line_list[1:]))

    # Sort bus stops by name
    bus_stops.sort(key=lambda tup: tup.name)
    return bus_stops


def get_all_predictions(stop_id: str) -> List[BusStopPrediction]:
    """
    Calls the ASEAG api (URA) to get all arrival predictions for a given bus stop.

    :param stop_id: String containing the api bus stop id
    :return: A list of all predictions at a given stop
    """
    payload = {"StopId": stop_id,
               "ReturnList": "StopId,LineName,DestinationText,EstimatedTime"}
    result = requests.get(config.base_url, params=payload)

    if result.status_code != 200:
        raise Exception("ASEAG api request returned status code %i" % result.status_code )

    predictions = []
    for line in result.text.splitlines():
        line_list = json.loads(line)

        # Line contains bus stop, if first entry is a '0'. Also remove test bus stops names '.'
        if line_list[0] == 1:
            predictions.append(BusStopPrediction(stop_id, *line_list[2:]))

    # Sometimes duplicates occur, therefore remove these
    predictions = list(set(predictions))
    predictions.sort(key=lambda tup: tup.estimated_time)

    return predictions
