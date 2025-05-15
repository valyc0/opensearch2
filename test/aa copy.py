import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor
import uuid
from threading import Lock
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # Importa il warning

# Disabilita il warning relativo alla verifica del certificato SSL
warnings.simplefilter('ignore', InsecureRequestWarning)

# Configurazione
OPENSEARCH_URL = "https://localhost:9200"  # URL del tuo server OpenSearch
USERNAME = "admin"  # Username per l'autenticazione
PASSWORD = "Matitone01!"  # Password per l'autenticazione
INDEX_NAME = "my_index"  # Nome dell'indice da usare
CONCURRENT_REQUESTS = 1   # Numero massimo di richieste simultanee
TEST_DURATION = 10         # Durata del test in secondi
REAL_TIME_INTERVAL = 1     # Intervallo per aggiornare i dati in tempo reale (secondi)

# Variabili globali
successful_requests = 0
total_requests = 0
lock = Lock()

# Documento di esempio
def generate_document():
    """Genera un documento di esempio da inviare a OpenSearch"""
    return {
        "id": str(uuid.uuid4()),
        "name": "Test User",
        "timestamp": time.time(),
        "value": 1234.56
    }

def send_insert_request():
    """Invia una richiesta di inserimento (indexing) al server OpenSearch."""
    global successful_requests, total_requests
    document = generate_document()
    try:
        response = requests.post(
            f"{OPENSEARCH_URL}/{INDEX_NAME}/_doc",
            json=document,
            auth=(USERNAME, PASSWORD),
            verify=False  # Disabilita la verifica del certificato SSL (solo per test)
        )
        response.raise_for_status()
        with lock:
            successful_requests += 1
    except Exception as e:
        print(f"Errore nella richiesta: {e}")
    finally:
        with lock:
            total_requests += 1

def real_time_monitor():
    """Stampa le statistiche in tempo reale."""
    global successful_requests, total_requests
    start_time = time.time()
    prev_successful = 0

    while time.time() - start_time < TEST_DURATION:
        time.sleep(REAL_TIME_INTERVAL)
        with lock:
            current_successful = successful_requests
            tps = current_successful - prev_successful
            prev_successful = current_successful
        print(f"[REAL-TIME] Inserimenti al secondo: {tps} | Totali riusciti: {current_successful}")

def run_test():
    """Esegue il test di inserimento."""
    global successful_requests, total_requests
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        monitor_thread = ThreadPoolExecutor(max_workers=1)
        monitor_thread.submit(real_time_monitor)
        while time.time() - start_time < TEST_DURATION:
            futures = [executor.submit(send_insert_request) for _ in range(CONCURRENT_REQUESTS)]

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\n--- RISULTATI ---")
    print(f"Richieste totali: {total_requests}")
    print(f"Richieste riuscite: {successful_requests}")
    print(f"Tempo totale: {elapsed_time:.2f} secondi")
    print(f"DPS (Documenti al secondo): {successful_requests / elapsed_time:.2f}")

if __name__ == "__main__":
    run_test()
