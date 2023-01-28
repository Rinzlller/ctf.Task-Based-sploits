#!/usr/bin/env python3
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('rusty')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

with open("rusty_ct", "rb") as data:
	flag_enc = data.read()[12:]

pt = b"a" * len(flag_enc)

io = start()
io.recvuntil(b"Here is ct:\n")
ct = io.recv()
# io.interactive()

key = [ p^c for p, c in zip(pt, ct) ]

print( "".join([ chr(k^f) for k, f in zip(key, flag_enc)]) )