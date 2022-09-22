# GDB cheat sheet
---

# GDB  basics
Changing to ***intel*** syntax
```bash
set disassembly-flavor intel
```
Finding the entry point and sections of a stripped binary
```bash
info file
```
View main function instructions
```bash
disassemble main
```
Setting a break point
```bash
break *main
break <ADDR> #0x00000000004005bd
```
Re-run the program
```bash
run <args> #(optional)
```
Stepping to the next instruction
```bash
si
```
Continue running the program
```bash
continue
```
View variables
```
info variables
x/s &<VAR>
```
View registers
```bash
info registers
info registers rip #(To view a specific register)
```
Set a value to a register
```bash
set $eax=0 # for example
```
Display formats

1. **`o`** => Display in octal.
2. **`x`** => Display in hexadecimal.
3. **`u`** => Display in unsigned, standard base-10 decimal.
4. **`t`** => Display in binary.

Example using examine command ( **`x`** ):
```bash
(gdb) x/o $rip
#0x55555555521b <main>:	037207407763
(gdb) x/x $rip
#0x55555555521b <main>:	0xfa1e0ff3
(gdb) x/u $rip
#0x55555555521b <main>:	4196274163
(gdb) x/t $rip
#0x55555555521b <main>:	11111010000111100000111111110011
```
 The default size of a single unit is a four-byte unit called a **`word`**,This can be changed by adding the following letters to the end of the examine command.
 1. **`b`** => A single byte.
2. **`h`** => A halfword, which is two bytes in size
3. **`w`** => A word, which is four bytes in size
4. **`g`** =>  A giant, which is eight bytes in size

Examples:
```bash
(gdb) x/8xb $rip
#0x55555555521b <main>:	0xf3	0x0f	0x1e	0xfa	0x55	0x48	0x89	0xe5
(gdb) x/8xh $rip
#0x55555555521b <main>:	0x0ff3	0xfa1e	0x4855	0xe589	0x8348	0x20ec	0x7d89	0x48ec
(gdb) x/8xw $rip
#0x55555555521b <main>:	0xfa1e0ff3	0xe5894855	0x20ec8348	0x48ec7d89
#0x55555555522b <main+16>:	0x64e07589	0x25048b48	0x00000028	0xf8458948
```
Examine command also accepts instruction ( **`i`** ) that display the memory as disassembled assembly language instructions.
```bash
(gdb) x/i $rip
#=> 0x55555555521b <main>:	endbr64 
(gdb) x/4i $rip
#=> 0x55555555521b <main>:	endbr64 
#   0x55555555521f <main+4>:	push   rbp
#   0x555555555220 <main+5>:	mov    rbp,rsp
#   0x555555555223 <main+8>:	sub    rsp,0x20
```
You can view vars