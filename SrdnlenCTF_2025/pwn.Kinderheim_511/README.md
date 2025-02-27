# Information

| CTF                                                 | Category | Solves | Points |
| --------------------------------------------------- | -------- | ------ | ------ |
| [Srdnlen CTF 2025](https://ctftime.org/event/2576/) | pwn      | 59     | 50     |

Description:

> Long live the expo. No wait, I mixed that one up. This is a remote challenge, you can connect to the service with: `nc k511.challs.srdnlen.it 1660`

- k511.elf

# Overview

Security status of the ELF:
```bash
─$ pwn checksec k511.elf        
[*] '~/SrdnlenCTF/pwn.Kinderheim_511/k511.elf'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

I reversed the ELF using IDA Pro and its Hex-Rays decomplier.

Functionality in the ELF:
- adding a new memory (allocate a new chunk in the heap),
- viewing a memory,
- removing a memory (freeing a chunk in the heap).

The flag is located in the 0th memory, which can neither be read nor deleted. The list of all memories is also located on the heap (right above the 0th memory).

# Vulnerability

When deleting a memory, it is possible to cause a situation where the memory (chunk) is freed in the heap, but the memory (chunk) address is not zeroed in the memories list. To do this, it is sufficient to first delete the `memories[i-1]`, and then delete the `memories[i]` → *hole in memory* situation.
```c
void erase_memory(char **memories, int id)
{
	int i;

	free(memories[id]);
	for ( i = 0; i <= id; ++i )
	{
		if ( !memories[i] )
		{
			puts("There's a hole in your memory somewhere...");
			return; // /!\ Stops at NULL pointer wihout zeroing the freed memories[i]
		}
		if ( id == i )
		{
			memories[i] = 0LL;
			printf("Erased at slot %d", (unsigned int)i);
			return;
		}
	}
	puts("Ran out of memory.");
}
```
The next `malloc` will return the address already in the memories list. This results in Use-After-Free and Double-Free.

# Exploiting

Plan of attack:
1. Reproducing Use-After-Free and leaking heap addresses:
	- calculate the address of the memories list,
	- calculate the address of the memory with the flag,
2. Preparing addresses in the memories list for Double-Free,
3. Exploiting Double-Free,
4. Allocating the next chunk in the heap over the memories list chunk and rewrite its addresses to the address of the memory with the flag,
5. Getting flag in memories with indices greater than zero.