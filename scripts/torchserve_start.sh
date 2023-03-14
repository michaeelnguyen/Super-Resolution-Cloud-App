#!/bin/bash

torchserve --start --ncs --model-store model-store --models all --ts-config config.properties &

while ! curl -s localhost:8080/ping; do sleep 60; done

./mtail --progs torchserve_custom.mtail --logs logs/model_metrics.log --logs logs/ts_metrics.log
