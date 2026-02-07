import socket
import re

class Scanner():
    
    ip_addr: str = ""
    port: int = 0

    def __init__(self, ip_addr: str, port: int):
        
        if ip_addr != "":
            # impostare una regex per controllare l'ipv4 o ipv6
            self.ip_addr = ip_addr
        if port >= 0:
            self.port = port
        return

    def getIpAddress() -> str:
        return self.ip_addr

    def setIpAddress(ip_addr: str) -> int:
        if ip_addr != "":
            # impostare una regex per ip
            self.ip_addr = ip_addr
        return 0

    def getPort() -> int:
        return self.port

    def setPort(port: int) -> int:
        if port >= 0:
            self.port = port
        return 0
    
    def grab_banner(s: socket):
        try:
            s.send(b"Hello\r\n")
            banner = s.recv(1024).decode().strip()
            return banner
        except:
            return "Nessun servizio riconosciuto"

    def scan_port(s: socket, timeout: float, ip_addr, port) -> int: 
    """ return the port number if the port is open
        or -1 on exception
        """
        try:    
            s.settimeout(timeout)
            result = s.connect_ex((ip_addr, port))

            if result == 0:
                return port
        except Exception as e:
            return -1

