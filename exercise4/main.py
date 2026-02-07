import socket
from concurrent.futures import ThreadPoolExecutor
import threading


IP_ADDR = "127.0.0.1"
PORT_RANGE = range(79, 81)

open_ports = []
ports_lock = threading.Lock()

def grab_banner(s):
    # Tenta di leggere la stringa di benvenuto del servizio
    try:
        s.send(b"Hello\r\n")
        banner = s.recv(1024).decode().strip()
        return banner
    except:
        return "Nessun servizio riconosciuto"

def scan_port(ip, port):
    # Tentativo di connessione ad una singola porta

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        
        # connect_ex restituisce 0 se la connessione ha avuto successo
        result = s.connect_ex((ip, port))
        
        if result == 0:
            banner = grab_banner(s)
            with ports_lock:
                open_ports.append((port, banner))
                print(f"[+] Porta: {port} - Banner: {banner}")

def avvia_scansione(target_ip, port_range):
    
    print(f"Scansione {target_ip} in corso...")
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in port_range:
            executor.submit(scan_port, target_ip, port)

    with open("scan_result.txt", "w") as f:
        f.write(f"Risultati per {target_ip}:\n")
        for p in sorted(open_ports):
            f.write(f"Porta {p}: APERTA\n")
    return

if __name__ == "__main__":
    avvia_scansione(IP_ADDR, PORT_RANGE)

