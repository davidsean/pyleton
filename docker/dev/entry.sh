#!/bin/bash

# wait for rabbitmq container
./docker/dev/wfi.sh -h rabbitmq -p 5672

python3 -m pyleton
