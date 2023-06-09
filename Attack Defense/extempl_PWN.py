#!/usr/bin/env python3

# $ pwn template ./rabbit.elf --host 109.233.56.90 --port 11617 > attack.py
from pwn import *

context.update(arch='i386')

flagRegEx = re.compile(r'[A-Za-z0-9]{31}=')

our_host = "10.80.3.2"      # define out host
port = 20000                # define port of service


def main():
    
    # host = "62.173.140.174 20000"          # DEBUG mode
    io = connect(host, port)

    hello = io.recvuntil(b'Type \'start\' to start a game')
    io.send(b'start\n')
    
    task = io.recvuntil(b'/100) ')
    print( task )

    # flag_list = flagRegEx.findall( home )
    
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