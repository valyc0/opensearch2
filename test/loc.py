import uuid
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Funzione per generare un documento di esempio
def generate_document():
    return {
        "id": str(uuid.uuid4()),
        "name": "Test User",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "value": 1234.56
    }

# Funzione per simulare l'inserimento di un documento
def simulate_insert_document(doc_id, data):
    start_time = time.time()
    time.sleep(0.001)  # Simula un ritardo di 1 millisecondo
    elapsed_time = time.time() - start_time
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Documento {doc_id} simulato in {elapsed_time:.4f} secondi.")

# Funzione per gestire l'inserimento con un rate limitato
def bulk_insert_simulation(config):
    num_documents = config['num_documents']
    rate_per_second = config['rate_per_second']
    max_workers = config['concurrent_requests']

    # Calcolare il delay tra le richieste per mantenere il rate desiderato
    delay_ms = 1000 / rate_per_second
    document_count = 0

    print(f"Avvio simulazione con rate desiderato: {rate_per_second} documenti/sec")
    print(f"Documenti totali da simulare: {num_documents}")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for i in range(1, num_documents + 1):
            data = generate_document()
            doc_id = data['id']

            # Invio del documento simulato
            futures.append(executor.submit(simulate_insert_document, doc_id, data))
            document_count += 1

            # Gestione del rate limit
            elapsed_time = time.time() - start_time
            elapsed_time_ms = elapsed_time * 1000
            if elapsed_time_ms < i * delay_ms:
                time.sleep((i * delay_ms - elapsed_time_ms) / 1000)

        # Attesa completamento delle simulazioni
        for future in futures:
            future.result()

    # Statistiche finali
    total_time = time.time() - start_time
    actual_rate = document_count / total_time
    print(f"\n--- Simulazione completata ---")
    print(f"Documenti simulati: {document_count}")
    print(f"Tempo totale: {total_time:.2f} secondi")
    print(f"Rate effettivo: {actual_rate:.2f} documenti/sec")
    print(f"Rate desiderato: {rate_per_second} documenti/sec")

if __name__ == "__main__":
    # Configurazione simulata
    config = {
        'num_documents': 5000,           # Numero di documenti da simulare
        'rate_per_second': 500,          # Rate massimo desiderato (documenti al secondo)
        'concurrent_requests': 5        # Numero massimo di richieste simultanee
    }

    # Esegui la simulazione di inserimento dei documenti
    bulk_insert_simulation(config)
