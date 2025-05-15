function add_hostname(tag, timestamp, record)
    -- Genera un hostname casuale
    local random_hostname = "host-" .. math.random(1000, 9999)
    -- Aggiungi il campo hostname al record
    record["hostname"] = random_hostname
    return 1, timestamp, record
end
