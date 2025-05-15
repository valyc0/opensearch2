# Kafka, Zookeeper e Kafka-UI con Docker Compose

Questo progetto configura un ambiente di sviluppo locale per Apache Kafka, Zookeeper e Kafka-UI utilizzando Docker Compose. È ideale per testare e sviluppare applicazioni che utilizzano Kafka.

## Componenti

1. **Zookeeper**: Un servizio centralizzato per la gestione della configurazione e la sincronizzazione dei nodi Kafka.
2. **Kafka**: Una piattaforma di streaming distribuita per la pubblicazione, sottoscrizione e elaborazione di flussi di dati in tempo reale.
3. **Kafka-UI**: Un'interfaccia web per monitorare e gestire i cluster Kafka.

## Configurazione

### File `docker-compose.yml`

Il file `docker-compose.yml` definisce tre servizi:

1. **Zookeeper**:
   - Immagine: `confluentinc/cp-zookeeper:7.5.0`
   - Porta esposta: `2181`
   - Variabili d'ambiente:
     - `ZOOKEEPER_CLIENT_PORT`: Porta di ascolto per i client (default: `2181`).
     - `ZOOKEEPER_TICK_TIME`: Frequenza di tick per il mantenimento della sessione (default: `2000` ms).

2. **Kafka**:
   - Immagine: `confluentinc/cp-kafka:7.5.0`
   - Dipende da: `zookeeper`
   - Porte esposte: `9092` (interno) e `19092` (esterno).
   - Variabili d'ambiente:
     - `KAFKA_BROKER_ID`: ID univoco del broker Kafka.
     - `KAFKA_ZOOKEEPER_CONNECT`: Connessione a Zookeeper (`zookeeper:2181`).
     - `KAFKA_LISTENERS`: Configurazione dei listener per connessioni interne ed esterne.
     - `KAFKA_ADVERTISED_LISTENERS`: Indirizzi pubblicizzati per i listener.
     - `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`: Mappa dei protocolli di sicurezza per i listener.
     - `KAFKA_INTER_BROKER_LISTENER_NAME`: Listener utilizzato per la comunicazione interna tra broker.
     - `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR`: Fattore di replica per il topic degli offset (default: `1`).

3. **Kafka-UI**:
   - Immagine: `provectuslabs/kafka-ui:latest`
   - Dipende da: `kafka`
   - Porta esposta: `8080`
   - Variabili d'ambiente:
     - `KAFKA_CLUSTERS_0_NAME`: Nome del cluster Kafka (default: `local`).
     - `KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS`: Indirizzo del broker Kafka (`kafka:9092`).

### Rete Docker

Tutti i servizi sono collegati a una rete Docker personalizzata chiamata `kafka-network`, che facilita la comunicazione tra i container.

---

## Come utilizzare

1. **Clona il repository** (se applicabile) o crea un file `docker-compose.yml` con il contenuto fornito.

2. **Avvia i servizi**:
   Esegui il seguente comando nella directory del progetto:
   ```bash
   docker-compose up -d
