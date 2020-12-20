#!/usr/bin/env bash
waitress-serve --port $PORT --call "covidWarnApp:create_app"
