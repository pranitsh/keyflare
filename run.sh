#!/bin/bash
source ./.venv/bin/activate
pip install -r ./requirements.txt
python3 ./keyflare/keyflare.py $1