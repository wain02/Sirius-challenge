#!/bin/bash

# Ejecutar la aplicación
if [ "$1" = "--api" ]; then
    exec python app.py --api
else
    exec python app.py
fi