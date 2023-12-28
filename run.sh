#!/usr/bin/env sh

# export environment variables
. /envs/env-local.sh

service postgresql start

# run python logic
python main.py
