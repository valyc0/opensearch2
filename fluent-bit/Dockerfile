# Usa Ubuntu 22.04 come base
FROM ubuntu:22.04

# Imposta le variabili ambientali per evitare interattività
ENV DEBIAN_FRONTEND=noninteractive

# Aggiorna il sistema e installa i prerequisiti
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Aggiungi la chiave GPG e il repository Fluent Bit
RUN sh -c 'curl https://packages.fluentbit.io/fluentbit.key | gpg --dearmor > /usr/share/keyrings/fluentbit-keyring.gpg' \
    && export CODENAME="jammy" \
    && echo "deb [signed-by=/usr/share/keyrings/fluentbit-keyring.gpg] https://packages.fluentbit.io/ubuntu/$CODENAME/ $CODENAME main" \
    | tee /etc/apt/sources.list.d/fluentbit.list

# Installa Fluent Bit
RUN apt-get update && apt-get install -y fluent-bit

# Porta di default per Fluent Bit
EXPOSE 2020

# Comando di default corretto per eseguire Fluent Bit
CMD ["/opt/fluent-bit/bin/fluent-bit", "-c", "/etc/fluent-bit/fluent-bit.conf"]
