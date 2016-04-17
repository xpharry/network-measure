# socket.select test
#!/usr/bin/env python 

""" 
An echo server that uses select to handle multiple clients at a time. 
Entering any line of input at the terminal will exit the server. 
""" 

import select 
import socket 
import sys 

host = '127.0.0.1' 
port = 33434 
backlog = 5 
size = 1024 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen(backlog) 
input = [server,sys.stdin] 
running = 1 
while running: 
    print "in loop now ..."
    inputready,outputready,exceptready = select.select(input,[],[],10) 
    print "in loop now ... ..."

    if len(inputready):
        for s in inputready: 

            if s == server: 
                print "s == server"
                # handle the server socket 
                client, address = server.accept() 
                input.append(client) 

            elif s == sys.stdin: 
                print "s == sys.stdin"
                # handle standard input 
                junk = sys.stdin.readline() 
                running = 0 

            else: 
                print "else"
                # handle all other sockets 
                data = s.recv(size) 
                if data: 
                    s.send(data) 
                else: 
                    s.close() 
                    input.remove(s) 
    else:
        print 'Timeout'
server.close()
