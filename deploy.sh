#!/bin/bash

# Install necessary packages
pip install dash dash-bootstrap-components pandas plotly gunicorn

# Start Dash application using Gunicorn
# app:server points to the server variable in app.py
gunicorn --workers 4 --bind 0.0.0.0:8050 app:server