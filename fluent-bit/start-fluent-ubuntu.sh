docker run -d --name fluentbit-container --net kafka_kafka-network \
-v $PWD/fluent-bit.conf:/etc/fluent-bit/fluent-bit.conf \
-v $PWD/data:/data \
-v /var/log:/var/log:ro \
fluent-bit-ubuntu22 /opt/fluent-bit/bin/fluent-bit -c /etc/fluent-bit/fluent-bit.conf
