docker run -d --name fluentbit-container --net mynet \
-v $PWD/fluent-bit.conf:/etc/fluent-bit/fluent-bit.conf \
-v $PWD/data:/data \
-v /var/log:/var/log:ro \
fluent-bit-ubuntu22 tail -f /dev/null

# Crea la directory /fluent-bit all'interno del container
docker exec fluentbit-container mkdir -p /fluent-bit

# Avvia Fluent Bit con il file di configurazione
docker exec fluentbit-container /opt/fluent-bit/bin/fluent-bit -c /etc/fluent-bit/fluent-bit.conf
