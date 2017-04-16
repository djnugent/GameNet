#!/bin/bash

sudo apt-get update -qq
sudo apt-get install --no-install-recommends -y \
build-essential \
g++ \
git \
tmux \
htop \
cmake \
python3 \
python3-dev \
python3-pip \
python3-setuptools \
python3-virtualenv \
python3-wheel \
pkg-config \
golang \
libjpeg-turbo8-dev \
make \
lsof \
zlib1g-dev \
docker

sudo apt-get clean


# pip installs
sudo pip3 --no-cache-dir install \
numpy \
scipy \
h5py \
pyyaml \
pydot \
opencv-python

#install gym
sudo pip3 --no-cache-dir install six
sudo pip3 --no-cache-dir install gym[atari]

#install universe
#rm -rf universe
#git clone https://github.com/openai/universe.git
#cd universe
#sudo pip3 --no-cache-dir install -e .
#cd ..
#sudo rm -rf universe
sudo pip3 --no-cache-dir install git+git://github.com/openai/universe.git@master

# Install tensorflow
sudo pip3 --no-cache-dir install tensorflow

# Install keras
sudo pip3 --no-cache-dir install keras

# Install keras-rl
sudo pip3 --no-cache-dir install git+git://github.com/matthiasplappert/keras-rl.git@master

#Install docker
./install_docker.sh
