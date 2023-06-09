#!/usr/bin/env python3

#===========================================================
#                       BxMCTF 2023
#===========================================================

from pwn import *
import os

exe = context.binary = ELF('./main.elf')

host = args.HOST or '198.199.90.158'
port = int(args.PORT or 37012)

def start_local(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

os.system('./crand.elf > rands.txt')
rands = open("rands.txt", "r").read().split("\n")[:-1]

io.recvuntil(b"Ok, it's time to do some math!\n")

for i in range(5):
    quest = io.recvline()
    answer = int(rands[i*2]) + int(rands[i*2+1])
    io.sendline( str(answer).encode() )

io.recvuntil(b"Ok, let's switch it up. This time you give me the first number, and I give the rest!\n")
for i in range(5, 10):
    quest = io.recvline()
    answer = int(rands[i*2+1]) - int(rands[i*2])
    io.sendline( str(answer).encode() )

io.interactive()

