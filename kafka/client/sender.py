import time
from confluent_kafka import Producer

# Configurazione del producer
producer_config = {
    'bootstrap.servers': 'localhost:19092',  # URL del broker Kafka
}

def delivery_report(err, msg):
    """Callback per la conferma di consegna."""
    if err is not None:
        print(f"Errore durante l'invio del messaggio: {err}")
    else:
        print(f"Messaggio inviato: {msg.key()} => {msg.value()}")

# Inizializzazione del producer
producer = Producer(producer_config)

topic = 'mytop'  # Nome della coda Kafka
messages_per_second = 5000  # Numero di messaggi al secondo
message_count = 0

try:
    print(f"Inizio invio di {messages_per_second} messaggi al secondo nella coda '{topic}'...")
    while True:
        start_time = time.time()
        for i in range(messages_per_second):
            key = f"key-{message_count}"
            value = f"message-{message_count}"
            producer.produce(
                topic,
                key=key,
                value=value,
                callback=delivery_report
            )
            message_count += 1

        # Attende che tutti i messaggi siano stati inviati
        producer.flush()

        # Calcola il tempo rimanente per completare il secondo
        elapsed_time = time.time() - start_time
        time_to_wait = max(0, 1 - elapsed_time)
        time.sleep(time_to_wait)

except KeyboardInterrupt:
    print("\nInterruzione da tastiera. Terminazione del programma...")

finally:
    # Chiude il producer
    producer.flush()
    print("Producer chiuso.")

