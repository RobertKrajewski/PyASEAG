########################################################################################################################
# ASEAG
base_url = "http://ivu.aseag.de/interfaces/ura/instant_V1"

########################################################################################################################
# app logic
# fuzzy match score have to be above this threshold to count as close match
bus_stop_name_matching_threshold = 85

########################################################################################################################
# Mattermost
mattermost_url = ''
mattermost_token = ""
icon_url = 'https://www.aseag.de/fileadmin/user_upload/images/Icons/routes_btn.png'
bot_name = "BusBot"

# default bus stop used if no query is given
default_bus_stop = "Bushof"
# number of matches presented to user if no close match is found
num_stop_matches = 3
# number of bus arrival predictions shown to the user
num_predictions = 10
# dictionary containing common errors and corrections to improve user experience
common_errors = {"hbf": "hauptbahnhof"}
