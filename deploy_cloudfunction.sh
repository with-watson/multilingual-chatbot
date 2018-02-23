#!/bin/bash
# IBM Think 2018
# multilingual-chatbot
# Deployment script for packaging and pushing cloud function

# constants
actionName="translator"
packageName="deployment.zip"
directoryName="cloudfunction"

# package
cd "$(dirname "$0")"/"$directoryName"
docker run --rm -v "$PWD:/tmp" openwhisk/python3action \
       bash  -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
zip -r "$packageName" virtualenv __main__.py

# deploy as action
bx wsk action update "$actionName" --kind python:3 "$packageName" --web true
