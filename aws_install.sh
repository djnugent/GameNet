apt-get update -qq
apt-get install --no-install-recommends -y \
    # install essentials
    build-essential \
    g++ \
    git \
    tmux \
    htop \
    cmake \
    # install python 3
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-virtualenv \
    python3-wheel \
    pkg-config \
    # universe requirements
    golang \
    libjpeg-turbo8-dev \
    make \
    lsof \
    zlib1g-dev \
    #docker runner
    docker \
 && apt-get clean


# pip installs
pip3 --no-cache-dir install \
    numpy \
    scipy \
    h5py \
    pyyaml \
    pydot \
    opencv-python

pip3 --no-cache-dir install six
pip3 --no-cache-dir install gym[atari]
pip3 --no-cache-dir install universe


# Install tensorflow
pip3 --no-cache-dir install tensorflow
#pip3 --no-cache-dir install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0-cp35-cp35m-linux_x86_64.whl

# Install keras
ARG KERAS_VERSION=1.2.1
ENV KERAS_BACKEND=tensorflow
#pip3 --no-cache-dir install --no-dependencies git+https://github.com/fchollet/keras.git@${KERAS_VERSION}
pip3 --no-cache-dir install keras

# Install keras-rl
pip3 --no-cache-dir install git+git://github.com/matthiasplappert/keras-rl.git@master
