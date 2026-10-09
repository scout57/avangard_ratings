#!/bin/bash


python -m notebook --allow-root --no-browser --port ${JYPUTER_PORT} --ip 0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
