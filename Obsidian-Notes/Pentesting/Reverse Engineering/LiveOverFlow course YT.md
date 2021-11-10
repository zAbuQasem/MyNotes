# LiveOverFlow course YT
---
# Navigation
1. **[[#GDB basics]]**
---

# GDB  basics
View main function instructions
```bash
disassemble main
```
Changing to ***intel*** syntax
```bash
set disassembly-flavor intel
```
Setting a break point
```bash
break *main
break <ADDR> #0x00000000004005bd
```
View registers
```bash
info registers
info registers rip #(To view a specific register)

```
Set a value to a register
```bash
set $eax=0 # for example :)
```
Stepping to the next instruction
```bash
ni
```
Re-run the program
```bash
run <args> #(optional)
```
Continue running the program
```bash
continue
```