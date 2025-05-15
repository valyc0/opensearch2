import uuid
import json
import time
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Disabilita il warning per connessioni HTTPS non verificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Funzione per caricare la configurazione dal file JSON
def load_config(config_file="config.json"):
    with open(config_file, "r") as f:
        return json.load(f)

# Funzione per generare un documento di esempio da inviare a OpenSearch
def generate_document():
    """Genera un documento di esempio da inviare a OpenSearch"""
    return {
        "id": str(uuid.uuid4()),  # Genera un ID unico utilizzando uuid4
        "name": "Test User",  # Nome dell'utente (esempio)
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),  # Timestamp formattato come stringa
        "value": 1234.56  # Un valore numerico esempio
    }

# Funzione per inviare l'inserimento di un documento
def insert_document(doc_id, data, config):
    url = f"{config['opensearch_url']}/{config['index_name']}/_doc/{doc_id}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, auth=(config['username'], config['password']), headers=headers, data=json.dumps(data), verify=False)  # Verifica disabilitata
        if response.status_code == 201:
            print(f"Documento {doc_id} inserito con successo.")
        else:
            print(f"Errore nell'inserimento del documento {doc_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Errore nella richiesta per il documento {doc_id}: {e}")

# Funzione per gestire l'inserimento in parallelo con un rate limitato
def bulk_insert(config):
    num_documents = config['num_documents']
    rate_per_second = config['rate_per_second']  # Rate di invio in documenti al secondo
    max_workers = config['concurrent_requests']
    
    # Calcolare il delay tra le richieste per mantenere il rate desiderato in millisecondi
    delay_ms = 1000 / rate_per_second  # Delay in millisecondi per mantenere il rate (1000 documenti al secondo -> 1ms)

    # Utilizziamo un ThreadPoolExecutor per inserire i documenti in parallelo
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        start_time = time.time()  # Tempo di inizio
        
        # Inserire i documenti dinamicamente con dati diversi
        for i in range(1, num_documents + 1):  # Inseriamo 'num_documents' documenti di prova
            data = generate_document()  # Generare i dati dinamici per ogni documento
            doc_id = data['id']  # L'ID del documento è generato nel documento stesso
            
            # Inserire il documento in parallelo
            futures.append(executor.submit(insert_document, doc_id, data, config))
            
            # Calcolare quanto tempo è passato e quanto aspettare per non superare il rate
            elapsed_time = time.time() - start_time
            elapsed_time_ms = elapsed_time * 1000  # Convertiamo in millisecondi
            if elapsed_time_ms < i * delay_ms:
                time.sleep((i * delay_ms - elapsed_time_ms) / 1000)  # sleep in secondi

        # Attendere il completamento di tutte le operazioni
        for future in futures:
            future.result()

if __name__ == "__main__":
    # Caricare la configurazione dal file
    config = load_config()
    
    # Esegui l'inserimento dei documenti
    bulk_insert(config)
