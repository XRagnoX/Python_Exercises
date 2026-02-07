from scapy.all import ARP, Ether, IP, IPv6,ICMPv6EchoRequest, ICMPv6ND_RS, ICMPv6ND_NS, ICMPv6NDOptSrcLLAddr, srp, sr
import json


ETH_BROADCAST = "33:33:00:00:00:01"
LINK_LOCAL_MULTICAST = "fe02::01"


def scan_network(ip_range):
    
    print(f"Scansione della rete {ip_range} in corso...")
    
    # Creaiamo il pacchetto ARP
    arp_request = ARP(pdst=ip_range)

    # Creaiamo il pacchetto Ethernet di Broadcast
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Uniamo i pacchetti
    packet = broadcast / arp_request

    # Inviamo e riceviamo risposte (Timeout 2.0s)

    # srp = Send and Receive Packets at Layer 2
    result = srp(packet, timeout=2, verbose=False)[0]
    
    devices = []
    for sent, received in result:
        devices.append({
                "ip": received.psrc,
                "mac": received.hwsrc,
            })
    return devices


# destination: ipv6 address
# scope: link interface
def ping_ipv6(destination: str, scope: str) -> list:
    
    # E.G.: ff02::1%eth0
    ip_addr = f"{destination}%{scope}"
    
    # IPv6 packet
    ip = IPv6(dst=ip_addr)
    er = ICMPv6EchoRequest()

    packet = Ether() / ip / er
    
    print("Invio Echo Request...")
    ans, unans = srp(packet, timeout=2, verbose=False)
    print(f"{ans.summary()}")
    # in alternativa 
    # ans, unans = sr(packet= ip / er)

    ping_responses = []
    for received, sent in ans:
        ping_responses.append({
                'ipv6': received[IPv6].src,
                'mac': received[Ether].src
            })
    return ping_responses


def ipv6_ns(mac_addr, ip_addr):
    
    eth = Ether(dst=f"{mac_addr}")
    ip = IPv6(dst=f"{ip_addr}")
    ns = ICMPv6ND_NS()

    packet = eth / ip / ns
    
    ans, unans = srp(packet, timeout=2, verbose=False)
    
    if ans.summary() is not None:
        neigh_device = []
        for received, sent in ans:
            neigh_device.append({
            'ip': received[IPv6].src,
            'mac': received[Ether].src
            })
    else:
        return None
    return neigh_device


def ns_request():
    # send a neighbour solicitation type 135

    eth = Ether(dst=ETHER_BROADCAST)
    ipv6 = IPv6(dst=LINK_LOCAL_MULTICAST, hlim=64)
    
    ns = ICMPv6ND_NS()
    
    packet = eth / ipv6 / ns
    
    ans, unans = srp(packet, timeout=2, verbose=False)
    
    if ans is not None:
        neighbours = []
        for received, sent in ans:
            neighbours.append([
                    {
                    'ipv6': received[IPv6].src,
                    'mac': received[Ether].src,
                    },
                    {
                    'ipv6': sent[IPv6].src,
                    'mac': sent[Ether].src,
                    }
                ])
    if len(neighbours) != 0:
        return neighbours   
    else:
        return None
    return None


def rs_request():
    # router solicitation type 133
    
    eth = Ether(dst=ETHER_BROADCAST)
    ipv6 = IPv6(dst=LINK_LOCAL_MULTICAST, hlim=64)

    rs = ICMPv6ND_RS()
    
    print("Inviando richiesta multicast RS...")
    ans, unans = srp(packet, timeout=2, verbose=False)

    if ans is not None:
        routers = []
        for received, sent in ans:
            routers.append({
                    'ipv6': received[IPv6].src,
                    'mac': received[Ether].src,
                })
    return routers


def scan_ipv6_local():
    # Destinazione ff02::1 e l'indirizzo multicast per tutti i nodi nel link-local
    # Questo pacchetto chiede "Chi e presente in questa rete"
    
    eth = Ether(dst=ETH_BROADCAST)
    ipv6 = IPv6(dst=LINK_LOCAL_MULTICAST, hlim=64)

    # ICMP EchoRequest (Ping)
    er = ICMPv6EchoRequest()
    packet = eth / ip / er

    print("Invio Echo Request...")
    # Invio del pacchetto su layer 2
    ans, unans = srp(packet, timeout=2, verbose=False)
    print(f"{ans.summary()}")
    
    if ans is not None:
        er_responses = []
        for received, sent in ans:
             er_responses.append({
                    'ipv6': received[IPv6].src,
                    'mac': received[Ether].src,
                })

    return er_responses


def test_function():

    # Il /24 indica la maschera di sottorete 255.255.255.0
    # Esempio per una classica sottorete casalinga
    risultati = scan_network("192.168.1.0/24")

    with open("dispositivi_rete.json", "w") as f:
        json.dump(risultati, f, indent=4)

    print(f"Trovati {len(risultati)} dispositivi su Ip_v4")
    
    routers = rs_request()
    if routers:
        raise Exception

    neighbours = ns_request()

    responses = scan_ipv6_local()

    with open("dispositivi_rete_ipv6.json", "w") as f:
        f.write("Routers: \n")
    with open("dispositivi_rete_ipv6.json", "a") as f:
        json.dump(routers, f, indent= 4)
        f.write(",\nNeghbour_Devices: \n")
        json.dump(neighbours, f, indent=4)

    print(f"{len(routers)} dispositivi Routers su Ip_v6")
    print(f"{len(neighbours)} dispositivi Neighbours Trovati nella sottorete")


def main():
    
    while True:
        opt = input("Option: ")
        if opt == "1":
            print("1. IPv4 ARP Request")
        elif opt == "2":
            print("2. Scan Neighbour")
        elif opt == "3":
            print("3. Scan Routers")
        elif opt == "4":
            print("4. ICMPv6 Echo Request")
        elif opt == "5" or opt == "-h" or opt == "--help":
            print("Help Table")
        elif opt == "6" or opt == "-q":
            print("Gracefull Exit.")
            return 
        else:
            print("Option not Found.")
    return


if __name__ == "__main__":
    main()

