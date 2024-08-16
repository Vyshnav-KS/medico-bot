#!/bin/sh

source .venv/bin/activate
export PYTHONPATH="$(pwd)"

pip install -r requirements.txt

cd server
uvicorn main:app --reload