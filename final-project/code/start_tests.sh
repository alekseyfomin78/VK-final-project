#!/bin/bash

pytest -s -v -l /tmp/code/api/tests/tests.py --alluredir=/tmp/alluredir
pytest -s -v -l /tmp/code/ui/tests/tests.py --alluredir=/tmp/alluredir