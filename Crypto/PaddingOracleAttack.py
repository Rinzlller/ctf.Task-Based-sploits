#!/usr/bin/env python3

import string
from pwn import *
from json import dumps

def main():

	s = remote("185.66.86.67", 4552)
	s.recv()
	print(2*"\n")

	################################
	
	ciphertext, iv = GetCiphertext()
	bl_size = 16
	
	plaintext = HackBlocks(ciphertext, iv, bl_size)	
	plaintext += HackFirstBlock(ciphertext, iv, bl_size)	

	data = dumps({
		"option": "verify_password",
		"password": str(plaintext)
	})
	print( data )
	s.sendline( data.encode() )
	r = s.recv().decode()
	print( r )

	################################

	print(2*"\n")
	s.close()	


def GetCiphertext() -> str:
	data = dumps({
		"option": "get_password"
	})
	s.sendline( data.encode() )
	r = s.recv().decode().split("\n")[0]
	
	get_password = eval(r)
	return get_password["ciphertext"], get_password["iv"]


def HackBlocks(ciphertext: str, iv: str, bl_size: int) -> str:
	plaintext = ""
	ciphertext = bytearray.fromhex(ciphertext)
	ciphertext_edit = bytearray.fromhex(ciphertext)
	iv = bytearray.fromhex(iv)
	middle = [0] * len(ciphertext)
	
	for n in range(len(ciphertext) - bl_size)[::-1]:
		valid_values = []

		for i in range( bl_size - n % bl_size - 1 ):
			ciphertext_edit[(n//bl_size+1)*bl_size - i - 1] = (bl_size - n % bl_size) ^ middle[(n//bl_size+1)*bl_size - i - 1]

		for i in range((n//bl_size+2)*bl_size, len(ciphertext)):
		 	ciphertext_edit[i] = bl_size

		for i in range(256):

			ciphertext_edit[n] = i

			if CheckPad(ciphertext_edit.hex(), iv.hex()):
				valid_values.append(i)
		
		if len(valid_values) == 2:
			x = valid_values[0] ^ valid_values[1] ^ ciphertext[n]
		else:
			x = valid_values[0]
		
		middle[n] = (bl_size - n % bl_size) ^ x
		plaintext = chr( middle[n] ^ ciphertext[n] ) + plaintext
		print( plaintext )

	return plaintext


def CheckPad(ciphertext: str, iv: str) -> bool:
	data = dumps({
		"option": "check",
		"text": ciphertext,
		"iv": iv
	})
	s.sendline( data.encode() )
	r = s.recv().decode().split("\n")[0]
	return r == "True"


def HakckFirstBlock(ciphertext: str, iv: str, bl_size: int) -> str:
	plaintext = ""
	iv_edit = bytearray.fromhex(iv)
	ciphertext = bytearray.fromhex(ciphertext)[:len(iv)]
	middle = [0] * len(iv)	

	for n in range(bl_size)[::-1]:

		for i in range( bl_size - n % bl_size - 1 ):
			iv_edit[bl_size - i - 1] = (bl_size - n) ^ middle[bl_size - i - 1]

		for i in range(256):

			iv_edit[n] = i

			if CheckPad(ciphertext.hex(), iv_edit.hex()):
				break

		middle[n] = i ^ (bl_size - n)
		plaintext = chr(middle[n] ^ iv[n]) + plaintext
		print( plaintext )	#w0w_p4dding_or4c

	return plaintext


if __name__ == "__main__":
    main()
