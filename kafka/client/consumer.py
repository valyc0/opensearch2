#!/usr/bin/env python
# filepath: /workspace/db-ready/opensearch2/kafka/client/consumer.py
import json
from confluent_kafka import Consumer, KafkaError

def main():
    # Configurazione del consumer
    consumer_config = {
        'bootstrap.servers': 'localhost:19092',  # Server Kafka aggiornato
        'group.id': 'python-consumer-group',
        'auto.offset.reset': 'earliest',  # 'latest' per leggere solo i nuovi messaggi
        'enable.auto.commit': True,
        'auto.commit.interval.ms': 1000  # Intervallo di commit automatico
    }

    # Inizializzazione del consumer
    consumer = Consumer(consumer_config)

    # Sottoscrizione al topic
    topic = 'mytopic-in'  # Nome del topic come definito in pipelines.yaml
    consumer.subscribe([topic])

    try:
        print(f"In ascolto di messaggi dal topic '{topic}'...\n")
        print("Premi CTRL+C per interrompere.")
        
        while True:
            # Poll per nuovi messaggi
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Fine della partizione, non è un errore
                    print(f"Raggiunta la fine della partizione {msg.partition()}")
                else:
                    # Errore
                    print(f"Errore: {msg.error()}")
            else:
                # Elaborazione del messaggio ricevuto
                key = msg.key().decode('utf-8') if msg.key() else "None"
                value = msg.value().decode('utf-8')
                
                # Tentativo di parsare il valore come JSON
                try:
                    value_json = json.loads(value)
                    print(f"Ricevuto messaggio:")
                    print(f"  Topic: {msg.topic()}")
                    print(f"  Partizione: {msg.partition()}")
                    print(f"  Offset: {msg.offset()}")
                    print(f"  Key: {key}")
                    print(f"  Value (JSON): {json.dumps(value_json, indent=2)}")
                except json.JSONDecodeError:
                    # Se non è JSON, mostra come stringa
                    print(f"Ricevuto messaggio:")
                    print(f"  Topic: {msg.topic()}")
                    print(f"  Partizione: {msg.partition()}")
                    print(f"  Offset: {msg.offset()}")
                    print(f"  Key: {key}")
                    print(f"  Value: {value}")
                
                print("-" * 50)

    except KeyboardInterrupt:
        print("\nInterruzione da tastiera. Terminazione del programma...")
    
    finally:
        # Chiusura del consumer
        consumer.close()
        print("Consumer chiuso.")

if __name__ == "__main__":
    main()
