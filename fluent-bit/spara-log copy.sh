#!/bin/bash

# Percorso del file di log
LOG_FILE="/var/log/aa.log"

# Verifica se il file esiste, altrimenti lo crea
if [ ! -f "$LOG_FILE" ]; then
  touch "$LOG_FILE"
fi

# Genera 10.000 righe
for i in $(seq 1 10000000); do
  echo "ipse dixit - riga numero $i" >> "$LOG_FILE"
done

echo "Generazione completata: 10.000 righe scritte in $LOG_FILE"

