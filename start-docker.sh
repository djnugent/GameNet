docker run --privileged --rm -it\
    -v /usr/bin/docker:/usr/bin/docker \
    -v /root/.docker:/root/.docker \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e DOCKER_NET_HOST=172.17.0.1 \
    -p 12345:12345 \
    -v `pwd`:/srv/ \
    universe
