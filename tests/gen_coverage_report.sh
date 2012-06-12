#!/bin/sh

rm .coverage
coverage run --source="sendhub" ./run_tests.py
coverage html -d coverage