#!/usr/bin/env bash

kill -9 $(ps aux | grep '[p]ython src/app.py' | awk '{print $2}')
python src/app.py --environment=development
