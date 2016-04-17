import select 
import socket 
import sys 
import time

import signal
import time
 
def test_request(arg=None):
    """Your http request."""
    time.sleep(2)
    return arg
 
class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

def main():
    port = 33434
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        #setup receive socket
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        recv_socket.bind(("", port))
        #recv_socket.settimeout(10)
        recv_socket.setblocking(0)
        ready = select.select([recv_socket], [], [], 10)
        print "size = " + str(len(ready))
    except socket.error , msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # tell kernel not to put in headers, when using IPPROTO_RAW this is not necessary
    # s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Get usable hostname
    destination_address = socket.gethostbyname('google.com')
    max_ttl = 50
    ttl = 1

    while(1):
        # Timer
        t_start = time.time()

        #s.sendto( (str(ttl)+'129.196.196.163'+destination_address), (destination_address , 0) ) 
        s.sendto( "", (destination_address , port) ) 

        # Receive and output
        # need to add, if no receive, timeout and increase ttl by one
        curr_addr = None
        curr_name = None
        try:
            if ready[0]:
                _, curr_addr = recv_socket.recvfrom(512)
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            else:
                with Timeout(3):
                    print 'Timeout'
        except Timeout.Timeout:
            print 'Timeout'
        except socket.error, e:
            print 'Socket Error. Error Code : ' + str(e[0]) + ' Message ' + e[1]
            sys.exit()

        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = "*"
        print "%d | %s | %dms" % (ttl, curr_host,(time.time()-t_start)*1000)

        ttl = ttl + 1

        if curr_addr == destination_address or ttl == max_ttl:
            s.close()
            recv_socket.close()
            break

if __name__ == "__main__":
    main()