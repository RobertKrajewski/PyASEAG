#!/usr/bin/env python

import json
import logging
from typing import List

from flask import request, Response, Flask, abort

import config
from app import logic, ura

app = Flask(__name__)

# Use gunicorn logger
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)


@app.route('/', methods=['POST'])
def handle_post():
    # Get all request data
    form = request.form
    try:
        token = form["token"]
        channel = form['channel_name']
        query = form['text']
        user_name = form['user_name']
        user_id = form['user_id']
        user_icon = config.mattermost_url + '/api/v4/users/' + user_id + '/image'
    except Exception as e:
        app.logger.error('Received invalid request: %s', str(form))
        abort(500)
        return

    # Check for valid Mattermost token if given
    if config.mattermost_token:
        if token != config.mattermost_token:
            app.logger.error('Received invalid token [%s]', token)
            return create_response(query + 'The integration is not correctly set up. The sent authentication '
                                           'token not valid. Please contact the administrator.', channel)

    if not len(query):
        app.logger.info('Using default query "%s"', config.default_bus_stop)
        query = config.default_bus_stop
    else:
        app.logger.info('Received query "%s"', query)

    # Handle request query
    try:
        predictions, stop_name = logic.predictions_by_stop_name(query)
        app.logger.info('Got %i predictions for bus stop "%s"', len(predictions), stop_name)
    except logic.NoMatchException as e:
        texts = ['No close match found for bus stop "%s". Potential matches:' % query]
        for match in e.closest_matches:
            texts.append("\n+ %s" % match[0])
        text = "".join(texts)
        app.logger.info(text.replace("\n", ""))
    except Exception as e:
        text = 'Query "%s" failed with exception: %s' % (query, str(e))
        app.logger.error(text)
    else:
        text = compose_prediction_table(predictions, stop_name)

    # Embed result in response and return to user
    return create_response(text, channel)


def compose_prediction_table(predictions: List[ura.BusStopPrediction], stop_name: str) -> str:
    """
    Creates a markdown table of all predictions to post in Mattermost.

    :param predictions: List of arrivals of at a given bus stop
    :param stop_name: name of the bus stop
    :return: String containing a markdown formatted table of all predictions.
    """
    if not len(predictions):
        text = ''.join('No arrivals at the bus stop **%s** in the next 90 minutes.' % stop_name)
    else:

        texts = list()
        texts.append('The next %d departures at the bus stop **%s**:  \n\n '
                     '|**Lane**|**Direction**|**Departure**| \n '
                     '|---:|:---|:---:|\n' % (config.num_predictions, stop_name))

        for line in predictions[:config.num_predictions]:
            depature_time = logic.unix_epoch_to_datetime(line.estimated_time)
            texts.append("|%s|%s|%.0f min (%s)|\n" % (line.line_name,
                                                      line.dest_name,
                                                      logic.datetime_timediff(depature_time),
                                                      depature_time.strftime("%H:%M")))

        text = "".join(texts)
    return text


def create_response(text: str, channel: str) -> Response:
    """
    Embeds a text in a flask Response ready to be given to flask.

    :param text: Text to embed in response.
    :param channel: Channel which should receive this response.
    :return: Response containing the text and directions how the response should look like.
    """
    payload = {'response_type': 'ephemeral',
               'channel': channel,
               'text': text,
               'username': config.bot_name,
               'icon_url': config.icon_url}

    resp = Response(
        json.dumps(payload),
        status=200,
        mimetype='application/json'
    )
    return resp


if __name__ == '__main__':
    # USE THIS LINE FOR DEBUGGING ONLY!
    app.run(host='0.0.0.0', debug=True)
