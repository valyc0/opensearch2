import requests
import time
from requests.auth import HTTPBasicAuth
import urllib3

# Disabilita il warning relativo alla connessione HTTPS non verificata
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurazione
OPENSEARCH_URL = "https://localhost:9200"
USERNAME = "admin"
PASSWORD = "Matitone01!"
INDEX_NAME = "my_index"  # Cambia con il nome del tuo indice
INTERVAL = 5  # Intervallo di monitoraggio in secondi
DEBUG = True  # Se True, stampa informazioni dettagliate

# Funzione per ottenere il numero di documenti nell'indice
def get_document_count():
    url = f"{OPENSEARCH_URL}/{INDEX_NAME}/_count"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)  # `verify=False` per ignorare problemi di certificato SSL
    if response.status_code == 200:
        count_data = response.json()
        return count_data['count']
    else:
        print(f"Errore nella richiesta: {response.status_code} - {response.text}")
        return 0

# Funzione per monitorare la velocità di inserimento dei documenti
def monitor_insertion_rate():
    previous_count = get_document_count()
    while True:
        time.sleep(INTERVAL)  # Aspetta per l'intervallo configurato
        current_count = get_document_count()
        
        if DEBUG:
            print(f"Documenti totali attuali: {current_count}")
        
        # Calcola la differenza dei documenti
        documents_per_second = (current_count - previous_count) / INTERVAL
        print(f"Documenti inseriti al secondo: {documents_per_second:.2f}")
        
        previous_count = current_count

if __name__ == "__main__":
    monitor_insertion_rate()
