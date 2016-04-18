# -*- coding: utf-8 -*-
#!/usr/bin/python

'''
    Our algorithm, at a high level, is an infinite loop whose body creates a connection,
    prints out information about it, and then breaks out of the loop if a certain condition
    has been reached.
'''

import socket
import struct
import select 
import sys
import time

# We want unbuffered stdout so we can provide live feedback for each TTL.
# You could also use the "-u" flag to Python.
class flushfile(file):
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

sys.stdout = flushfile(sys.stdout)


class Tracer:
    def __init__(self, dest_name):
        # Turn a hostname into an IP address.
        self.dest_name = dest_name
        self.dest_addr = socket.gethostbyname(dest_name)
        self.port = 33434
        self.ttl = 32
        self.max_hops = 30
        self.max_wait = 3.0
        self.nqueries = 3
        self.reached = 0

        self.open_sockets()

    def trace(self):
        self.reached = 0
        while self.ttl:
            delta = []
            for i in range(self.nqueries):
                send_at = self.send_probe(self.ttl)
                reply, recv_at = self.get_reply()
            if reply:
                delta = recv_at - send_at
            else:
                delta = -1

            self.display_results(delta)
            if self.reached:
                break


    def open_sockets(self):
        # Create sockets for the connections.
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Build the GNU timeval struct (seconds, microseconds)
        timeout = struct.pack("ll", 5, 0)
        # Set the receive timeout so we behave more like regular traceroute
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
        # Set the TTL field on the packets.
        self.send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, self.ttl)

        # Bind the sockets and send some packets.
        self.recv_socket.bind(("", self.port))
        self.send_socket.sendto("", (self.dest_name, self.port))

    def build_probe_packet(self, dest):
        pass

    def send_probe(self, ttl):
        start_time = time.time()
        self.send_socket.sendto("python - geometry distance measurement", (self.dest_name, self.port))
        return start_time

    def get_reply(self):
        timeout = self.max_wait

        while True:
            # use select() to check the availability of the site
            inputready, outputready, exceptready = select.select([self.recv_socket], [], [], timeout)

            # Test for timeout
            if inputready:
                try:
                    packet, curr_addr = recv_socket.recvfrom(4096)
                    finished = True
                    curr_addr = curr_addr[0] # intermediate hosts' IP address
                    try:
                        curr_name = socket.gethostbyaddr(curr_addr)[0]
                    except socket.error:
                        curr_name = curr_addr
                except socket.error as (errno, errmsg):
                    sys.stdout.write("* ")

                arrive_time = time.time()
                _reply = ip.Packet(packet)
                reply = icmp.Packet(_reply.data)

            if reply.type != icmp.ICMP_UNREACH:
                self.reached = 1
                return _reply, arrive_time
            timeout = (start + self.max_wait) - time.time()
            if timeout < 0:
                return None, None

    def display_results(self, delta):
        print "time elapsed = %f" % delta


def main(dest_name):
    tracer = Tracer(dest_name)
    tracer.trace()

if __name__ == "__main__":
    main('google.com')