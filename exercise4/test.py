import socket
import threading

IP_ADDR = "127.0.0.1"
PORT = 80
SERVER_NAME = "VeryRealServer"

def handle_client(conn, addr, service_name):
    
    try:
        banner = f"Welcome to {service_name} Server v1.0\r\n"
        conn.send(banner.encode())
        print(f"Banner Sent...")
    finally:
        conn.close()


def avvia_server(ip, port, name):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((ip, port))
    server.listen(5)
    
    print(f"[*] Servizio '{name} attivo sulla porta {port}'")

    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(conn, addr, name), daemon=True).start()
        


avvia_server(IP_ADDR, PORT, SERVER_NAME)

