#!/bin/bash

# Percorso del file di log
LOG_FILE="/var/log/aa.log"

# Verifica se il file esiste, altrimenti lo crea
if [ ! -f "$LOG_FILE" ]; then
  touch "$LOG_FILE"
fi

# Numero totale di righe da generare
TOTAL_LINES=10000000

# Rate di scrittura (righe al secondo)
RATE=1

# Calcola il tempo di attesa tra le righe (in secondi)
SLEEP_TIME=$(echo "scale=6; 1 / $RATE" | bc)

# Genera le righe
echo "Inizio generazione di $TOTAL_LINES righe a un rate di $RATE righe/secondo"
for ((i = 1; i <= TOTAL_LINES; i++)); do
  # Ottieni la data e ora correnti
  CURRENT_DATE=$(date '+%Y-%m-%d %H:%M:%S')
  
  # Scrive la riga con la data e l'ora nel file di log
  echo "$CURRENT_DATE - Ipse dixit lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip. - riga numero $i" >> "$LOG_FILE"
  
  # Pausa per rispettare il rate di 1 riga al secondo
  sleep "$SLEEP_TIME"
done

echo "Generazione completata: $TOTAL_LINES righe scritte in $LOG_FILE"

