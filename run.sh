#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source $SCRIPT_DIR/.venv/bin/activate

if [ $# -eq 0 ]; then
    echo "Running"
    python3 $SCRIPT_DIR/keyflare/keyflare.py
else
    if [[ "$1" == "install" ]]; then
        echo "Performing Install"
        pip install -r $SCRIPT_DIR/requirements.txt
        echo "Running"
        python3 $SCRIPT_DIR/keyflare/keyflare.py
    else
        echo "Starting with $1 number of clicks"
        python3 $SCRIPT_DIR/keyflare/keyflare.py "${@}"
    fi    
fi
