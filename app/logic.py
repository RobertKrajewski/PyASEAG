import datetime
from fuzzywuzzy import process
from typing import List, Tuple
from app import ura
import config


class NoMatchException(Exception):
    """
    Exception raised if no good match between query string and available bus stops is found. The variable
    closest_matches contains tuples of potential matches and the matching score in descending order.
    """
    def __init__(self, closest_matches):
        super().__init__(self)
        self.closest_matches = closest_matches


def predictions_by_stop_name(query: str) -> Tuple[List[ura.BusStopPrediction], str]:
    """
    Get all arrival predictions for a single bus stop specified by query string. After determining the most matching bus
    stop candidate by fuzzy string matchting, predictions are received. Exceptions are raised if no or only bad matches
    for the query are found.

    :param query: String containing the name of a bus stop.
    :return: List containing all bus arrival predictions given by the ASEAG api.
    """
    # Get all stops
    bus_stops = ura.get_all_stops()

    # Replace typical phrases in query for better performance
    for old, new in config.common_errors.items():
        query = query.replace(old, new)

    # Find matching stop name
    stop_names = [stop.name for stop in bus_stops]
    stop_matches = process.extract(query.lower(), stop_names, limit=config.num_stop_matches)

    if len(stop_matches) == 0:
        raise Exception("No matching stop name found for query %s" % query)
    elif stop_matches[0][1] < config.bus_stop_name_matching_threshold:
        raise NoMatchException(stop_matches)

    # Get best match
    best_match_name = stop_matches[0][0]
    best_match_id = [bus_stop.id for bus_stop in bus_stops if bus_stop.name == best_match_name][0]

    # Get predictions
    predictions = ura.get_all_predictions(best_match_id)

    return predictions, best_match_name

import datetime

def unix_epoch_to_datetime(epoch_ms):
    return datetime.datetime.fromtimestamp(epoch_ms/1000)


def datetime_timediff(dt):
    now = datetime.datetime.now()
    if now > dt:
        return 0.0
    else:
        return (dt-now).seconds/60.0