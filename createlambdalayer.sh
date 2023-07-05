#!/bin/bash

if [ "$1" != "" ] || [ $# -gt 1 ]; then
  echo "Creating layer compatible with python version $1"

  docker run -v "$PWD":/var/task "lambci/lambda:build-python$1" /bin/sh -c "pip install -r requirements.txt -t python/lib/python$1/site-packages/; exit"

  if [ -d "python" ]; then
    rm -r python
  fi

  7z a -r ../lambda_function.zip * -xr!__pycache__*

  if [ -f "../lambda_function.zip" ]; then
    echo "Done creating layer!"
    ls -lah ../lambda_function.zip
  else
    echo "Failed to create layer. Check the zip command and its arguments."
  fi

else
  echo "Enter python version as an argument - ./createlayer.sh 3.6"
fi
