docker run -it --rm --name  fluentbit-container --net mynet \
-v $PWD/fluent-bit.conf:/etc/fluent-bit/fluent-bit.conf \
-v $PWD/data:/data \
-v /var/log:/var/log:ro \
fluent-bit-ubuntu22 bash

docker exec -it fluentbit-container

