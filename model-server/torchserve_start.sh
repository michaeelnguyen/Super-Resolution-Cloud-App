#!/bin/bash

# Mount Torchserve directory to Azure Blob Storage using blobfuse2
blobfuse2 mount /torchserve --config-file=./config.yaml

sleep 20

rsync -av --exclude='mtail' --exclude='tmp/' --exclude='logs/config/' /home/model-server /torchserve/model-server-backup

torchserve --start --ncs --model-store model-store --models all --ts-config config.properties &

while ! curl -s localhost:8080/ping; do sleep 60; done

./mtail --progs torchserve_custom.mtail --logs logs/model_metrics.log --logs logs/ts_metrics.log

