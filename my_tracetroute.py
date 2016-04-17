# -*- coding: utf-8 -*-
#!/usr/bin/python

'''
    Our algorithm, at a high level, is an infinite loop whose body creates a connection,
    prints out information about it, and then breaks out of the loop if a certain condition
    has been reached.
'''

import socket
import sys
import time

def main(dest_name):
    # Turn a hostname into an IP address.
    dest_addr = socket.gethostbyname(dest_name)

    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')

    port = 33434
    max_hops = 30

    ttl = 1 # TTL field
    while True:
        # Create sockets for the connections.
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)

        # Set the TTL field on the packets.
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        # Bind the sockets and send some packets.
        recv_socket.bind(("", port))
        send_socket.sendto("", (dest_name, port))

        sys.stdout.write(" %d  " % ttl) # ?

        # Get the intermediate hosts' IP addresses.
        curr_addr = None
        curr_name = None

        finished = False ##
        tries = 3 ##

        while not finished and tries > 0:
            try:
                _, curr_addr = recv_socket.recvfrom(512)
                finished = True
                curr_addr = curr_addr[0] # intermediate hosts' IP address
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error as (errno, errmsg):
                tries = tries - 1
                sys.stdout.write("* ")

        send_socket.close()
        recv_socket.close()

        # Turn the IP addresses into hostnames and print the data.
        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = "*"
            
        sys.stdout.write("%s\n" % (curr_host))

        ttl += 1

        # End the loop.
        # two conditions for exiting our loop — 1. reached our destination
        #                                       2. exceeded some maximum number of hops.
        if curr_addr == dest_addr or ttl > max_hops:
            break

if __name__ == "__main__":
    main('google.com')