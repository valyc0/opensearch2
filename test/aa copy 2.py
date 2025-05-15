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

# Funzione per gestire l'inserimento in parallelo, mantenendo il rate di 100 richieste al secondo
def bulk_insert(config):
    num_documents = config['num_documents']
    rate_limit = 100  # Limite di 100 richieste al secondo
    time_interval = 1 / rate_limit  # Pausa tra le richieste per rispettare il rate
    
    # Utilizziamo un ThreadPoolExecutor per inserire i documenti in parallelo
    with ThreadPoolExecutor(max_workers=config['concurrent_requests']) as executor:
        futures = []
        
        # Inserire i documenti dinamicamente con dati diversi
        for i in range(1, num_documents + 1):  # Inseriamo 'num_documents' documenti di prova
            doc_id = i
            data = generate_document()  # Generare i dati dinamici per ogni documento
            
            # Inserire il documento in parallelo
            futures.append(executor.submit(insert_document, doc_id, data, config))
            
            # Pausa per mantenere il rate di 100 documenti al secondo
            time.sleep(time_interval)
        
        # Attendere il completamento di tutte le operazioni
        for future in futures:
            future.result()

if __name__ == "__main__":
    # Caricare la configurazione dal file
    config = load_config()
    
    # Esegui l'inserimento dei documenti
    bulk_insert(config)
