#!/bin/bash

# Activate the Elastic Beanstalk Python virtual environment
source /var/app/venv/*/bin/activate

# Upgrade pip, setuptools, and wheel to avoid install/build errors
pip install --upgrade pip setuptools wheel