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

# Calcola il tempo di attesa tra i batch
BATCH_SIZE=1000  # Numero di righe per batch
SLEEP_TIME=$(echo "scale=6; $BATCH_SIZE / $RATE" | bc)

# Genera le righe
echo "Inizio generazione di $TOTAL_LINES righe a un rate di $RATE righe/secondo"
for ((i = 1; i <= TOTAL_LINES; i++)); do
  echo "Ipse dixit lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip. - riga numero $i" >> "$LOG_FILE"
  
  # Pausa ogni BATCH_SIZE righe
  if ((i % BATCH_SIZE == 0)); then
    sleep "$SLEEP_TIME"
  fi
done

echo "Generazione completata: $TOTAL_LINES righe scritte in $LOG_FILE"
