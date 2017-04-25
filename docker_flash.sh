#!/bin/bash
BLUE='\033[0;34m'
NC='\033[0m' # No Color

python train.py --env-id flashgames.NeonRace-v0 --num-workers 2 --log-dir ../../neonrace
echo -e "${BLUE}Connect to vnc at $(curl -s ipinfo.io/ip):5900 with password: openai${NC}"
echo -e "${BLUE}Or${NC}"
echo -e "${BLUE}Connect to vnc at $(curl -s ipinfo.io/ip):15900/viewer/?password=openai${NC}"
