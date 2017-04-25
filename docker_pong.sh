#!/bin/bash
BLUE='\033[0;34m'
NC='\033[0m' # No Color

python3 train.py --env-id gym-core.PongDeterministic-v3 --num-workers 2 --log-dir ../pong
echo -e "${BLUE}Connect to vnc at $(curl -s ipinfo.io/ip):5900 with password: openai${NC}"
echo -e "${BLUE}Or${NC}"
echo -e "${BLUE}Connect to vnc at $(curl -s ipinfo.io/ip):15900/viewer/?password=openai${NC}"
