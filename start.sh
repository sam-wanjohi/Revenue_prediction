#!/usr/bin/env bash
uvicorn scripts.api:app --host 0.0.0.0 --port $PORT
