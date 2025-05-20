#!/bin/bash
# Start Data Prepper per connettere Kafka a OpenSearch

# Assicurati che il container sia fermato se già in esecuzione
docker stop data-prepper || true
docker rm data-prepper || true

# Avvia Data Prepper con la configurazione corretta
docker run --name data-prepper \
--net host \
  -v $PWD/config/pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml \
  -v $PWD/config/data-prepper-config.yaml:/usr/share/data-prepper/config/data-prepper-config.yaml \
  -p 4900:4900 \
  opensearchproject/data-prepper:latest

echo "Data Prepper avviato con connessione da Kafka a OpenSearch"
