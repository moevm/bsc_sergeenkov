#!/bin/bash

python download_model.py
gunicorn --bind 0.0.0.0:5000 encoder:app