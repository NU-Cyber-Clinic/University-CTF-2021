# Vault

1. File is a 32-bit ELF Linux binary
2. Running it with no arguments gives this prompt
```
┌──(kali㉿kali)-[~/Downloads/rev_vault]
└─$ ./vault
Could not find credentials
```
3. Getting pseudocode from Ghidra we can see it tries to open a file called `flag.txt`
```cpp
    _ZNSt14basic_ifstreamIcSt11char_traitsIcEEC1EPKcSt13_Ios_Openmode(fileStream,"flag.txt",8);
                    /* try { // try from 0010c25e to 0010c400 has its CatchHandler @ 0010c2a5 */
    isFileOpen = _ZNSt14basic_ifstreamIcSt11char_traitsIcEE7is_openEv(fileStream);
    if ((isFileOpen & 1) == 0) {
        print(&std::cout,"Could not find credentials\n");
                        /* WARNING: Subroutine does not return */
        exit(-1);
    }
```
NOTE: the variable names have been assigned by me. The decompiler just assigned them an identifier in the format of `local_10`, `local_11`, etc.
4. Creating `flag.txt` in the same folder and running `vault` will give this result
```
┌──(kali㉿kali)-[~/Downloads/rev_vault]
└─$ ls -la
total 1628
drwxr-xr-x  2 kali kali    4096 Nov 23 13:48 .
drwxr-xr-x 15 kali kali    4096 Nov 21 11:07 ..
-rw-r--r--  1 kali kali      91 Nov 21 05:34 flag.txt
-rwxr-xr-x  1 kali kali   96584 Oct 19 11:56 vault
                                                
┌──(kali㉿kali)-[~/Downloads/rev_vault]
└─$ ./vault
Incorrect Credentials - Anti Intruder Sequence Activated...
```
5. Checking through the code we can see that it checks if the first 25 (`0x19`) characters are `good`, meaning that the stream has not failed or is not the end of file. It basically checks whether or not the file has at least 25 characters in it
```cpp
isStreamGood = true;
i = 0;
while( true ) {
    isCharGood = 0;
    if (i < 0x19) {
        isCharGood = _ZNKSt9basic_iosIcSt11char_traitsIcEE4goodEv
                                ((long)fileStream + *(long *)(fileStream[0] + -0x18));
    }
                    /* If any of the characters are not valid, break. */
    if ((isCharGood & 1) == 0) break;
    _ZNSi3getERc(fileStream,&weirdVariable);
    isFileOpen = (***(code ***)(&PTR_PTR_00117880)[(byte)(&DAT_0010e090)[(int)i]])();
    if ((int)weirdVariable != (uint)isFileOpen) {
        isStreamGood = false;
    }
    i = i + 1;
}
```
6. This snippet is essentially a for loop doing what is mentioned in step 5. The weirder bit is this one
```cpp
    isFileOpen = (***(code ***)(&PTR_PTR_00117880)[(byte)(&DAT_0010e090)[(int)i]])
```
7. We can see in assembly that it actually uses something called `vtables` to call a different function by its offset in memory rather than using a function name. It also uses the `i` counter to iterate through the different offsets.
8. It's easier to see this in IDA's assembly graph where instead of a subroutine, it calls the function at the address stored in `rcx` which is changed with each iteration.
```assembly
loc_559AF6171353:
    movsxd  rcx, [rbp+i]
    lea     rsi, unk_559AF6173090
    movzx   ecx, byte ptr [rcx+rsi]
    mov     esi, ecx
    lea     rcx, off_559AF617C880
    mov     rdi, [rcx+rsi*8]
    mov     rcx, [rdi]
    mov     rcx, [rcx]
    call    rcx ; This is where each value is called, set a breakpoint here
    mov     cl, al
    mov     [rbp+isFileOpen], cl
    jmp     $+5
```
9. In the `flag.txt` file add 25 random characters so that the `for` iteration can get through all functions in the vtable.
10. Run the executable with a breakpoint set at `call rcx` and step in. 
11. With every iteration we can see a hardcoded value in each function. 
```assembly
.text:000056448CD6D260 push    rbp
.text:000056448CD6D261 mov     rbp, rsp
.text:000056448CD6D264 mov     [rbp+var_8], rdi
.text:000056448CD6D268 mov     al, 48h ; 'H'
.text:000056448CD6D26A movzx   eax, al
.text:000056448CD6D26D pop     rbp
.text:000056448CD6D26E retn
.text:000056448CD6D26E sub_56448CD6D260 endp
```
12. Every value is a different character from the final flag which is 
```
HTB{vt4bl3s_4r3_c00l_huh}
```
