#!/data/data/com.termux/files/usr/bin/python3

import socket
import sys
import os
from threading import Thread
import encryptor as enc
import codecs
# Part 9
# Developing a TCP Network Proxy - Pwn Adventure 3
# https://www.youtube.com/watch?v=iApNzWZG-10

class Client(Thread):

    def __init__(self, host, port, seed, mod):
        super(Client, self).__init__()
        self.seed = seed
        self.mod = mod
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        print("Waiting for clients on port", str(sys.argv[1])+"!")
        self.client, self.addr = sock.accept()

    def run(self):
        while True:
            data = self.client.recv(4096)
            if data:
                #print("[{}] -> {}".format(self.port, data.__repr__()))
                try:
                    print("<- client["+str(self.addr[0])+"]:", enc.decrypt(data.decode(), self.seed, self.mod))
                except Exception as e:
                    print('client[{}]'.format(self.addr[0]), e)


if len(sys.argv) < 2:
    print("Usage: \"python3 server.py <listen port>\"")
    exit(1)

try:
    print("Generating encryption secret...")
    _, seed, mod = enc.encrypt("a"*128)
    #print("[DEBUG]", _.__repr__(),seed,mod)

    print("Encryption secret:", str(seed)+"$"+str(mod))

    client = Client("0.0.0.0", int(sys.argv[1]), seed, mod)
    client.start()


    while True:
        try:
            cmd = input(': ')
            if cmd == 'quitquit':
                exit(0)
            client.client.sendall(enc.complex_encrypt(cmd, client.seed, client.mod).encode())
            print("-> client["+client.addr[0]+"]:", cmd)
        except Exception as e:
            print(e)

except KeyboardInterrupt:
    print("\nCTRL+C detected, Quitting!")
    try:
        client.client.close()
    except:
        pass
    exit(0)

except Exception as err:
    print("\nSomething went wrong!")
    print("Error message:",err)
    exit(1)
