#!/usr/bin/env python

# Copyright 1997, Corporation for National Research Initiatives
# written by Jeremy Hylton, jeremy@cnri.reston.va.us

import ip, icmp, udp
import socket
import select
import time
import os
import getopt
import string

# We want unbuffered stdout so we can provide live feedback for each TTL.
# You could also use the "-u" flag to Python.
class flushfile(file):
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

sys.stdout = flushfile(sys.stdout)

''' main class used in this traceroute program '''
class Tracer:

    def __init__(self, dest_name):
		self.port = 33434
		self.max_hops = 30
		self.max_wait = 3.0

		# Turn a hostname into an IP address.
    	self.dest_addr = socket.gethostbyname(dest_name)

    def open_sockets(self):   	
        # Create sockets for the connections.
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)

	    icmp = socket.getprotobyname('icmp')
	    udp = socket.getprotobyname('udp')

        # Set the TTL field on the packets.
        self.send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        # Build the GNU timeval struct (seconds, microseconds)
        timeout = struct.pack("ll", 5, 0) # ?
        
        # Set the receive timeout so we behave more like regular traceroute
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout) # ?

    def init_probe_packet(self, src, dest):
    	pass

    def send_probe(self, seq, ttl):
		now = time.time()
		return now

    def get_reply(self, seq):
	start = time.time()
	timeout = self.max_wait
	while 1:
	    ready, write, error = select.select([self.recv_socket], [], [], timeout)
	    if ready:
            # use select() to check the availability of the site
            sys.stdout.write(" %d  " % ttl) # ?

            # Get the intermediate hosts' IP addresses.
            curr_addr = None
            curr_name = None

            finished = False ##
            nqueries = 3 ##

            while not finished and nqueries > 0:
                try:
                    _, curr_addr = self.recv_socket.recvfrom(4096)
                    elapsed_time = time.time() - start_time
                    finished = True
                    curr_addr = curr_addr[0] # intermediate hosts' IP address
                    try:
                        curr_name = socket.gethostbyaddr(curr_addr)[0]
                    except socket.error:
                        curr_name = curr_addr
                except socket.error as (errno, errmsg):
                    nqueries = nqueries - 1
                    sys.stdout.write("* ")

                arrive = time.time()
                
            self.send_socket.close()
            self.recv_socket.close()

            # Turn the IP addresses into hostnames and print the data.
            if curr_addr is not None:
                curr_host = "%s (%s)" % (curr_name, curr_addr)
            else:
                curr_host = ""

            sys.stdout.write("%s " % (curr_host))
            if elapsed_time:
                sys.stdout.write("%f\n" % (elapsed_time))
            else:
                sys.stdout.write("%s\n" % "")

            ttl += 1
		
    def trace(self):
	seq = 0
	self.got_there = 0
	for ttl in range(1, self.max_ttl+1):
	    deltas = []
	    hosts = {}

    def trace_summary(self, ttl, host, deltas):
		pass







class CollectorTracer(Tracer):
    
    def __init__(self, host):
	Tracer.__init__(self, host)
	self.results = {}

    def trace_summary(self, ttl, host, deltas):
	self.results[ttl] = (host, deltas)
	
class CmdlineTracer(Tracer):
    
    def __init__(self, host):
	Tracer.__init__(self, host)
	self.resolve_host = 1
	self.output_style = 2

    def trace_summary(self, ttl, host, deltas):
	if resolve_host:
	    try:
		name, aliases, ipaddr = socket.gethostbyaddr(host)
		if aliases:
		    name = aliases[0]
	    except socket.error:
		name = host
	    print " %d  %s (%s) " % (ttl, name, host),
	else:
	    print " %d  %s" % (ttl, host),
	if output_style == 2:
	    print "\n\t",
	for delta in deltas:
	    if delta > 0.:
		print " %7.3f ms  " % (delta),
	    else:
		print "    *        ",
	print
    


def usage():
    usage = \
"""Usage: traceroute.py [-m max_ttl] [-n] [-p port] [-q nqueries] [-w wait] [-s]
                 host
"""
    print usage

def parse_options(args, tracer):
    opts, args = getopt.getopt(args, 'snm:p:q:w:')
    for k, v in opts:
	if k == '-n':
	    tracer.resolve_host = 0
	elif k == '-s':
	    tracer.output_style = 1
	elif k == '-m':
	    try:
		hops = string.atoi(v)
		tracer.max_ttl = hops
	    except ValueError:
		print "invalid max_ttl value", v
		return []
	elif k == '-p':
	    global def_port
	    try:
		port = string.atoi(v)
		tracer.def_port = port
	    except ValueError:
		print "invalid port", v
		return []
	elif k == '-q':
	    try:
		n = string.atoi(v)
		tracer.nqueries = n
	    except ValueError:
		print "invalid number of queries", v
		return []
	elif k == '-w':
	    try:
		w = string.atoi(v)
		tracer.max_wait = float(w)
	    except ValueError:
		print "invalid timeout", w
		return []
    return args
    
def main():
    import sys
    t = CmdlineTracer(host[0])
    host = parse_options(sys.argv[1:], t)
    if len(host) != 1:
	usage()
	return
    t.open_sockets()
    t.trace()

if __name__ == "__main__":
    main()
