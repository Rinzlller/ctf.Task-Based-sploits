# Information

| CTF                                                       | Task         | Category | Solves | Points |
| --------------------------------------------------------- | ------------ | -------- | ------ | ------ |
| [VolgaCTF 2025 Qualifier](https://ctftime.org/event/2676) | Baby-Welcome | pwn      | 16     | 331    |

Description:
> *Privet!*

Attachments:
- baby-welcome.zip
	- Dockerfile
	- baby-welcome (ELF 64-bit)

# Overview

Security status of the ELF:
```bash
─$ pwn checksec baby-welcome        
[*] '/home/kali/VolgaCTF/pwn.baby-welcome/baby-welcome'
    Arch:       amd64-64-little
    RELRO:      Full RELRO       🟩
    Stack:      Canary found     🟩
    NX:         NX enabled       🟩
    PIE:        PIE enabled      🟩
    Stripped:   No               🟥
```

I reversed the ELF using IDA Pro and its Hex-Rays decomplier.

Functionality in the ELF:
- register a new user,
- login,
	- send a message to another user,
	- read all my messages,
	- logout,
- exit.

Based on the Dockerfile, the flag is located on the file system at path `/flag-7df861f08550278f45228533773d1663.txt`.

# Vulnerability

Classic format string vulnerability when user tries to read all his messages.
```c
void __fastcall print_messages()
{
  message *message_i;

  for (
    message_i = current_user->messages;
    message_i;
    message_i = message_i->next_message
  )
    printf(message_i->text); //   /!\ Format-String vuln

  putchar('\n');
}
```

# Exploiting

Because of *Full RELRO* we are forced to exploit ret2libc attack.

Luckily, when the `print_messages` function (exactly `printf`) is executed, there is an `rbp` on the stack, and this `rbp` points to another `rbp` that places over the `ret`  address that will be used when the `main` function exit:
```python
+---print_messages---+
|  0xDEADBEEFCAFEBABE|
|  0xDEADBEEFCAFEBABE|
|  0xDEADBEEFCAFEBABE|
|                rbp __    ← target address
|                ret |  \
+---auth_handlers----+  |
|  0xDEADBEEFCAFEBABE|  |
|  0xDEADBEEFCAFEBABE|  |
|  0xDEADBEEFCAFEBABE|  |
|                rbp ___/  ← target
|                ret |  \
+--------main--------+  |
|  0xDEADBEEFCAFEBABE|  |
|  0xDEADBEEFCAFEBABE|  |
|  0xDEADBEEFCAFEBABE|  |
|                rbp ___/
|                ret |
+--------------------+
```

So we can rewrite `auth_handlers`'s `rbp` and point it to our ROP payload on the stack.

Plan of attack:
1. Leak stack and libc addresses via *read primitive* (f-string vuln).
	1. Register two users.
	2. Send payload from one to another.
	3. Trigger payload.
2. Put the ROP chain (exactly *one gadget*) on the stack.
	1. Add ROP chain right after password and zero-byte when login.
3. Rewrite `rbp` to ROP chain address via *write primitive* (f-string vuln).
	1. Send payload from one to another.
	2. Trigger payload.
4. Trigger ROP chain by exit from `main`.