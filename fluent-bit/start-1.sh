#!/bin/bash

# Percorso del file di log
LOG_FILE="./data/aa.log"

# Verifica se il file esiste, altrimenti lo crea
if [ ! -f "$LOG_FILE" ]; then
  touch "$LOG_FILE"
fi

# Numero totale di righe da generare
TOTAL_LINES=10000000

# Tempo di attesa tra le righe (1 secondo)
SLEEP_TIME=1

# Genera le righe
echo "Inizio generazione di $TOTAL_LINES righe a un rate di 1 riga/secondo"
for ((i = 1; i <= TOTAL_LINES; i++)); do
  # Ottieni la data e ora correnti
  CURRENT_DATE=$(date '+%Y-%m-%d %H:%M:%S')
  
  # Scrive la riga con la data e l'ora nel file di log
  echo "$CURRENT_DATE - Ipse dixit lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip. - riga numero $i" >> "$LOG_FILE"
  
  # Pausa per rispettare il rate di 1 riga al secondo
  sleep "$SLEEP_TIME"
done

echo "Generazione completata: $TOTAL_LINES righe scritte in $LOG_FILE"
