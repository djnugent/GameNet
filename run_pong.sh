#!/bin/bash
BLUE='\033[0;34m'
NC='\033[0m' # No Color

python3 train.py --env-id gym-core.PongDeterministic-v3 --num-workers 32 --log-dir ../../pong
echo " "
echo " "
echo -e "${BLUE}Connect to vnc at $(curl ipinfo.io/ip):5901 with password: openai${NC}"

