#!/usr/bin/env bash

gunicorn integrations/mattermost:app \
    --workers 4 \
    --bind 0.0.0.0:9000 \
    --log-file /var/log/busbot.log \
    --log-level INFO \
    --reload