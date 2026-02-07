from scapy.all import IP, IPv6, ICMPv6EchoRequest, ICMPv6ND_NS, Ether, srp
import json


def ns_req(ip_addr):
    
    eth = Ether()
    ip = IPv6(dst=ip_addr, hlim=64)

    ns = ICMPv6ND_NS()
    
    packet = eth / ip / ns

    ans, unans = srp(packet, timeout=2, verbose=False)

    if ans is not None:
        neighbours = []
        for received, sent in ans:
            neighbours.append([{
                    'ipv6': received[IPv6].src,
                    'hlim': received[IPv6].hlim,
                    'mac': received[Ether].src,
                },
                {
                    'ipv6': sent[IPv6].src,
                    'hlim': sent[IPv6].hlim,
                    'mac': sent[Ether].src,
                }
                               ])
    return neighbours


def hops_mapping_v6(ip_addr, ttl: int):     

    route_nodes = []
    for hop in range(0, ttl):
        
        eth = Ether()
        ipv6 = IPv6(dst=ip_addr, hlim=hop)
        er = ICMPv6EchoRequest()

        packet = eth / ipv6 / er

        ans, unans = srp(packet, timeout=2, verbose=False)
        
        for received, sent in ans:
            route_nodes.append([
                                {'ip': sent[IPv6].src,
                                 'hlim': sent[IPv6].hlim,
                                 'mac': sent[Ether].src,
        
                                }, 
                                {'ip': received[IPv6].src, 
                                'hlim': received[IPv6].hlim,
                                'mac': received[Ether].src,
                                   }
                                ])
    return route_nodes

TEST_IPv6 = 'fe80::f0cb:7eff:fead:b02c'

#nodes = hops_mapping('fe80::f0cb:7eff:fead:b02c', 4)
#for node in nodes:
#    print(f"{node}")

try:
    neighbours = ns_req(TEST_IPv6)
    with open('./neighbours.json', 'w') as f:
        json.dump(neighbours, f, indent=4)
except Exception as e:
    print(e)
finally:
    print('Gracefull Exit')

