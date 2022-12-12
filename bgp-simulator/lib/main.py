from time import sleep

from scapy.all import *
import scapy.all as scapy
from scapy.layers.inet import IP, ICMP, Ether
from scapy.layers.l2 import ARP

from lib.router import Router
from lib.wire import Wire
from lib.interface import Interface

#i1 = Interface('172.16.1.1', 30)
#i2 = Interface('172.16.1.2', 30)
#i3 = Interface('172.16.10.1', 30)
#i4 = Interface('172.16.10.2', 30)
#
#
#wire = Wire()
#wire2 = Wire()
#
#i2.connect_wire(wire)
#i1.connect_wire(wire)
#
#i3.connect_wire(wire2)
#i4.connect_wire(wire2)
#
#r1 = Router('r1', 501)
#r2 = Router('r2', 502)
#r3 = Router('r3', 503)
#
#r1.add_interface(i1)
#r1.add_interface(i3)
#
#r2.add_interface(i2)
#r3.add_interface(i4)
#
#r1.set_bgp('172.16.1.1', 'On', 502, '172.16.1.2')
##r1.set_bgp('172.16.10.1', 'On', 503, '172.16.10.2')
#r2.set_bgp('172.16.1.2', 'On', 501, '172.16.1.1')
##r3.set_bgp('172.16.10.2', 'On', 501, '172.16.10.1')
#
#control_list = []
#control_list.append(r1.on())
#control_list.append(r2.on())
#control_list.append(r3.on())
#
#c = 0
#while True:
#    c += 1
#    if c > 2000:
#        break
#
#    sleep(1)
#
#r1.off()
#r2.off()
#r3.off()
#
#for i in control_list:
#    i.join()

def init(routers, wires, interfaceMap):

    logicRouters = {}
    logicInterfaces = {}

    for router in routers.values():
        name = router.properties["name"]
        as_id = router.properties["as_id"]
        logicRouters[as_id] = Router(name, int(as_id))

    for interface in interfaceMap.values():
        ip = interface.source
        mask = interface.mask
        logicInterfaces[ip] = Interface(ip, mask)
        parentRouter = logicRouters[interface.router.properties["as_id"]]
        parentRouter.add_interface(logicInterfaces[ip])

    for wire in wires:
        interface1 = logicInterfaces[wire.interface1.source]
        interface2 = logicInterfaces[wire.interface2.source]
        logicWire = Wire()
        interface1.connect_wire(logicWire)
        interface2.connect_wire(logicWire)

        parentRouter1 = interface1.device
        parentRouter2 = interface2.device
        parentRouter1.set_bgp(interface1.ip, 'On', parentRouter2, interface2.ip)
        parentRouter2.set_bgp(interface2.ip, 'On', parentRouter1, interface1.ip)

    control_list = []

    for router in logicRouters.values():
        control_list.append(router.on())

    c = 0
    while True:
        c += 1
        if c > 2000:
            break

        sleep(1)

    for router in logicRouters.values():
        router.off()

    for i in control_list:
        i.join()

def test_send():
    packet = IP(dst="8.8.8.8", ttl=20) / ICMP()
    #Ether()/IP()/TCP()
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24")
    answer, pp = scapy.sr(packet, timeout=20)
    for s, r in answer:
        if r.haslayer(IP):
            resp = IP(raw(r))
            print(export_object(resp))
