#!/bin/bash
echo "Starting to trigger gunicorn"
cd ./src && gunicorn --bind  0.0.0.0:5000 application:app & 
sleep 5
echo "Starting Nginx Service"
nginx -g 'daemon off;'