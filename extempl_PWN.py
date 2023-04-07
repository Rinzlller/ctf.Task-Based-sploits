#!/usr/bin/env python3

# $ pwn template ./rabbit.elf --host 109.233.56.90 --port 11617 > attack.py
from pwn import *

context.update(arch='i386')

our_host = "10.80.3.2"      # define out host
port = 31337                # define port of service

def main():
    
    host = "10.80.4.2"          # DEBUG mode
    io = connect(host, port)

    io = start()

    status = io.recvline()
    io.send(b'123\n')
    
    status = io.recvline()
    print( status )
    
    io.interactive()


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        print(f"Usage: python3 {sys.argv[0]} <host>")
        sys.exit(-1)
    
    if host == our_host:
        sys.exit(-4)
    
    main()