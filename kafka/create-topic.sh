#!/bin/bash

# Crea il topic utilizzando il container Kafka definito nel docker-compose.yml
docker exec -it kafka /bin/kafka-topics --create --bootstrap-server kafka:9092 \
--topic mytopic-in \
--partitions 10 \
--replication-factor 1

echo "Topic mytopic-in creato con successo" 