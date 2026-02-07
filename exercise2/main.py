import socket
import json
import re
import queue
import threading

from datetime import datetime


IP_ASCOLTO = "127.0.0.1"
PORTA_ASCOLTO = 5140
FILE_LOG = "logs_convertiti.json"

coda_log = queue.Queue()

def worker_scrittura():
    # il thread che si occupa di scrivere i log sul file
    print("[Worker] Thread di scrittura avviato")
    while True:
        # Preleva un log dalla coda, si blocca finche non c'e qualcosa
        log_data = coda_log.get()
        if log_data is None: # Segnale di chiusura
            break
        
        try:
            with open(FILE_LOG, "a") as f:
                f.write(json.dumps(log_data) + "\n")
        except Exception as e:
            print(f"Errore scrittura file: {e}")
        finally:
            coda_log.task_done()

def parse_syslog(data):
    """
    Estrae dati da una stringa Syslog

    Formato atteso: <PRI>TIMESTAMP HOSTNAME APP: MESSAGGIO
    """
    pattern = r"<(.*?)>(.*?) (.*?) (.*?): (.*)"
    match = re.search(pattern, data)

    if match:
        return {
            "priority": match.group(1),
            "timestamp_raw": match.group(2),
            "hostname": match.group(3),
            "app_name": match.group(4),
            "message": match.group(5),
            "processed_at": datetime.now().isoformat(),    
            }
    return {"raw_data": data, "error": "Formato non riconosciuto"}

def avvia_server():
    # Avviamo il Thread di scrittura come Daemon
    thread_writer = threading.Thread(target=worker_scrittura, daemon=True)
    thread_writer.start()

    # Creazione del socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP_ASCOLTO, PORTA_ASCOLTO))
    
    print(f"Server in ascolto su {IP_ASCOLTO}:{PORTA_ASCOLTO}...")
    print(f"Premi CTRL+C per fermare")

    try:
        while(True):
            data, addr = sock.recvfrom(1024)
            messaggio_raw = data.decode('utf-8')
            
            log_strutturato = parse_syslog(messaggio_raw)
            log_strutturato["client_ip"] = addr[0]
            
            coda_log.put(log_strutturato)

            print(f"Log ricevuto da {addr[0]} e salvato")

    except KeyboardInterrupt:
        print("\nServer Arrestato.")
        coda_log.put(None)
        thread_writer.join()
        sock.close()
    finally:
        sock.close()    


if __name__ == "__main__":
     avvia_server()

