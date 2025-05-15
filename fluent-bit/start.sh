docker run -it --rm --net mynet --name fluentbit \
-v $(pwd)/fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf \
-v $PWD/log:/data/log \
fluent/fluent-bit:3.2
