# Writeups Index

There are all my CTF sploits derived by categories and topics

# PWN

<details>
  <summary><strong>Buffer Overflow</strong></summary>

  - BOF → [UTCTF 2025. secbof](https://github.com/Rinzlller/ctf.Task-Based-sploits/tree/main/UTCTF_2025/pwn.secbof)
    > *...Simply Buffer Overflow with **ROP** and **seccomp**. Seccomp allows us to use `open`, `read`, `write` and `exit`...*

</details>

<details>
  <summary><strong>Fromat String</strong></summary>

  - rbp-rbp-rbp → [Volga CTF 2025 Qualifier. Baby-Welcome](https://github.com/Rinzlller/ctf.Task-Based-sploits/tree/main/VolgaCTF_2025_Qualifier/pwn.baby-welcome)
    > *...Classic format string vuln... rewrite function's rbp and point it to our ROP payload on the stack...*

</details>

<details>
  <summary><strong>Heap</strong></summary>

  - Double Free → [Srdnlen CTF 2025. Kinderheim 511](https://github.com/Rinzlller/ctf.Task-Based-sploits/tree/main/SrdnlenCTF_2025/pwn.Kinderheim_511)
    > *...the memory (chunk) is freed in the heap, but the memory (chunk) address is not zeroed in the memories list...*

</details>

<details>
  <summary><strong>Shellcoding</strong></summary>

  - Length limitations → [Volga CTF 2025 Qualifier. sbsbx](https://github.com/Rinzlller/ctf.Task-Based-sploits/tree/main/VolgaCTF_2025_Qualifier/pwn.sbsbx)
    > *...sequential reading of three shellcodes with **length limitations**. **Seccomp** denies us to use `read`, `execve` and `execveat`...*

</details>