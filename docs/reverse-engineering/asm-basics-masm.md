## ASM basics
---
## Navigation

- **[[#Intel instructions]]**
- **[[#Basic data types]]**
	1. [[#Legacy data directives]]
	2. [[#Data definition statement]]
	3. [[#Defining BYTE SBYTE data]]
	4. [[#Defining Byte Arrays]]
	5. [[#Defining strings]]
- **[[#Instructions]]**
- **[[#Operand types]]**
- **[[#Data Transfer Instructions]]**
	- **[[#MOV instruction]]**
		- [[#MOV errors]]
		- [[#Zero extension]]
		- [[#Sign extension]]
	- **[[#XCHG instruction]]**
		- [[#Examples]]
- **[[#Data related operators and directives]]**
	- [[#Align directive]]
	- [[#PTR operator]]
	- [[#TYPE operator]]
	- [[#LENGTHOF operator]]
	- [[#SIZEOF operator]]
	- [[#Multiple lines and anonymous data]]
	- [[#LABEL directive]]
	- [[#OFFSET operator]]
	- [[#ESI register]]
	- [[#PTR for indirect addressing]]
	- [[#Indirect operand variable as a pointer]]
	- [[#Array sum example]]
	- [[#JMP instructions]]
	- [[#LOOP instruction]]
- **[[#References]]**
---
# Basic elements
1. **[[#Integer constants and expressions]]**
2. **[[#Character and string]]**
3. **[[#Reserved words and identifiers]]**
4. **[[#Directives موجه]]**
5. **[[#Labels]]**
6. **[[#Mnemonic]]**

![Nasm structure.png](../assets/Reverse%20Engineering/Nasm%20structure.png)

## Integer constants and expressions.
- Optional leading `+` or `-` sign.
- Binary, Decimal, Hexadecimal.
- Common radix characters:
	- `h` => hexadecimal  (Use as much as possible)
	- `d` => Decimal  (When hex makes no sense)
	- `b` => Binary  (For bitwise clarity)
	- `r` => Encoded real  (Real)
**Examples:**
`30d`, `6Ah`, `42`, `1101b`

>**NOTE:** Hexadecimal can't begin with a letter. => 0A2h

### Expressions
As any programming language
```txt
(2*3) + 4/6
```
---
## Character and string
- **Enclose character in single or double quotes.**
	-  `'a'` , `"a"`  => (ASCII char == 1 byte).
- **Enclose strings in single or double quotes.**
	- `"Hello"` , `'Hello'` => (Each ASCII char == 1 byte).
- **Embedded quotes are allowed**
	- `'Say "Abuqasem" is learning'`
	- `"This isn't  a test"`

> **NOTE:**
> Each string must end with a  '0' to tell the function to print until the zero.
> => "Hello world",0 (old assemblers used '$' instead of zero)

---
## Reserved words and  identifiers
- **Reserved words cannot be used as identifiers.**
	- Instruction mnemonics, directives,  type attributes, operators, predefined symbols.
- **Identifiers**
	- 1-247 chars, including digits.
	- Not case sensitive.
	- First character must be a letter. => (`_`, `@`, `?`, `$`)
	- Used for labels (Procedure names, variables, constants).
---
## Directives (موجه)
- **Instructions on how to assemble (Not at runtime).**
- **Commands that are recognized ad acted upon by the assembler.**
	- Not part of the intel instruction set.
	- Used to declare code , data areas, select memory model, declare procedures, variables etc..
	- Not case sensitive (.data,.DATA,.DAta).
- **Different assemblers have different directives**
	- GNU , netwide are not the same as MASM.
- **One important function of assembler directives is to define program sections, or segments**
	- .data (define variables)
	- .code (write code)
	- .stack 100h
 ---
 ## Labels
 - **Act as a place markers**
 	- Marks the address (offset) of code ad data.
 - **Follow identifier rules**
 - **Data label (Variable names)**
 	- Must be unique.
 	- `count DWORD 100` => (not followed by a colon)
 - **Code label**
 	- Target of jump and loop instructions.
 	- `L1:`  => (Followed by a colon)
 --- 
 ## Mnemonic
 - **No operands**
 	- `stc` => (set carry flag)
 - **One operand**
 	- `inc eax` => (register)
 	- `inc myByte` => (memory)
 - **Two operands**
 	- `add ebx,ecx` => (register, register)
 	- `sub myByte,25` => (memory, constant)
 	- `add eax,36 * 25` => (register, const-expr)

### NOP instruction
- No Operation.
- Uses 1 byte of storage.
- CPU: Reads it, Decodes it, ignores it.
- Used to allign code to even-address boundaries (multiple of 4):
```txt
0  mov ax,5
3  nop      ; alligns next instruction
4  add ax,8
```
- x86 processors are designed to load code and data more quickly from even-doubleword addresses.

 ---
## Intel instructions
- **Assembled into machine code by assembler and executed at runtime by CPU.**
- **An instruction contains:**
	- Label => (Optional)
	- Mnemonic => (Required)
	- Operands => (Depends on the instruction)
	- Comment => (Optional) begins with a ';' 

```txt
[label:] mnemonic [operands] [;comment]

loop1: 
mov eax,32 ; this is a comment
```
---
# Basic data types
1. `BYTE`, `SBYTE`: 8-bit unsigned & signed integers.
2. `WORD`, `SWORD`: 16-bit unsigned & signed integers.
3. `DWORD`, `SDWORD`: 32-bit unsigned & signed integers.
4. `QWORD`: 64-bit integer. => (Not signed/unsigned)
5. `TBYTE`: 80-bit integer. => (ten byte)
6. `REAL4`, `REAL8`: 4-byte & 8-byte long reals.
7. `REAL10`: 10-byte IEEE extended real.
## Legacy data directives
1. `DB`: 8-bit integer.
2. `DW`: 6-bit integer.
3. `DD`:  32-bit integer or real.
4. `DQ`: 64-bit integer or real.
5. `DT`: 80-bit integer. => (ten bytes).

## Data definition statement
1. A data definition statement sets aside storage in memory for a variable.
2. May optionally assign a name (label) to the data.
- **Syntax**
![variable statement.png](../assets/Reverse%20Engineering/variable%20statement.png)
3. Use the `?` symbol for undefined variables.
4. All initializers become binary data in memory.
## Defining BYTE, SBYTE data
- **Each of the following defines a single byte of storage.**
1. `Value1 BYTE 'A'` => character constant.
2. `Value2 BYTE 0` => smallest unsigned byte. 
3. `Value3 BYTE 255` => largest unsigned byte.
4. `Value4 SBYTE -128` => smallest signed byte.
5. `Value5 SBYTE +127` => largest signed byte.
6. `value6 BYTE ?` => uninitialized byte.
- The optional name is label marking the variable's offset from the beginning of it's enclosing segment.
- If value1 is located at `offset 0000` in the data segment and consumes 1 byte of storage, value2 is automatically located at `offset 0001`
- If you declare a `SBYTE` variable, the microsoft debugger will automatically display it's value in decimal with a leading sign.
## Defining Byte Arrays
![offset.png](../assets/Reverse%20Engineering/offset.png)
1. An array is simply a set of sequential memory locations.
2. The directive (BYTE) indicates the offset needed to get to the next array element.
3. No length, no termination flag, no special properties.
## Defining strings
- A string is implemented as a sequence of characters.
	1. For convenience, it's usually enclosed in quotation  marks.
	2. It's usually null terminated.
	3. Characters are bytes.
	4. Hex characters `0Dh`(CR) and `0Ah`(LF) are useful.
- **Example**
![define strings.png](../assets/Reverse%20Engineering/define%20strings.png)

---
# Instructions
## Outline
1. **Data Transfer Instructions**
	- Operand types
	- `MOV`, `MOVZX`, `MOVSX`
	- `LAHF`, `SAHF`
	- `XCHG`
2. **Addition and Subtraction**
	- `INC`, `DEC`
	- `ADD`, `SUB` 
	- `NEG`
3. **Data-related operators and directives**
4. **Indirect addressing**
5. `JMP`, `LOOP`

## Operand types
1. Immediate (constant integer(8,16,32 bits))
2. Register (the name of register)
3. Memory (reference to location in memory)
	- Memory address is encoded with the instruction, or a register holds the address of a memory location
```txt
.data
	var1 BYTE 10h
;suppose var1 were located at offset 10400h
MOV AL,var1 ; AL 00010400
```
### Operand notation
![operand notation.png](../assets/Reverse%20Engineering/operand%20notation.png)
# Data Transfer Instructions
## MOV instruction
1. Move from source to destination
	- `MOV destination, source`
2. Both operands must be the same size.
3. **No more** than one memory operand permitted.
4. `CS`, `EIP`, `IP` **cannot** be the destination.
5. **No immediate** to segment registers moves.
6. To `MOV` memory to memory.
```txt
.code
	MOV AX,var1
	MOV var2,AX
```
7. Direct memory operands
```txt
.data
	var1 BYTE 10h
.code
	MOV AL, var1 ; AL = 10h
	MOV AL,[var1] ; AL = 10h 
	
; Use it only when an arithmetic expression is involved
MOV AL, [var1 + 5]
```
### MOV errors
```txt
.data
	bVal 	BYTE 	100
	bVal2 	BYTE 	?
	wVal 	WORD 	2
	dVal 	DWORD 	5

.code
	MOV AL,wVal		; byte <- word
	MOV AX,bVal		; word <- byte
	MOV EAX,bVal	; dword <- byte
	MOV DS,45		; immediate value not permitted
	MOV EIP,dVal	; invalid destination (EIP)
	MOV 25,bVal		; invalid destination (25)
	MOV bVal2,bVal	; move in mem not permitted
```
### Zero extension
- When you copy a smaller value into a larger destination, the `MOVZX` instruction fills (extends) the upper half of the destination with zeros.
![zeroext.png](../assets/Reverse%20Engineering/zeroext.png)
### Sign extension
- The `MOVSX` instruction fills the upper half of the destination with a copy of the source operand's sign bit.
![signext.png](../assets/Reverse%20Engineering/signext.png)
## XCHG instruction
1. XCHG exchanges the values of two operands.
2. At least **one operand** must be a register.
3. No immediate operands are permitted.
```txt
.data
	var1 WORD 1000h
	var2 WORD 2000h

.code
	XCHG AX,BX		; exchange 16-bit regs
	XCHG AH,AL		; exchange 8-bit regs
	XCHG var1,BX	; exchange mem, reg
	XCHG EAX,EBX	; exchange 32-bit regs
	
	XCHG var1,var2	; Error: two memory operands
```
## Examples
- [Explained here](https://www.youtube.com/watch?v=BRY2e7kFkD4&list=PLMm8EjqH1EFVodghdDWaAuHkHqj-nJ0bN&index=16)
```txt
.data
	arrayW	WORD 1000h,2000h,3000h
	arrayD	DWORD 1,2,3,4
	
.code
	MOV AX,[arrayW+2]	; AX = 2000h
	MOV AX,[arrayW+4]	; AX = 3000h
	MOV AX,[arrayW+6]	; EAX = 000000002h
	MOV EAX,[arrayD+4]
	
	MOV AX,[arrayD-2]	; AX = 3000h
	MOV EAX,[arrayD+20]	; Possible seg fault!
```
> 1. There is no "range checking" - the address is calculated and used.
> 2. Size of transfer is based on the destination.

### Example 2
- Write a program that adds the following three bytes:
```txt
.data
	myBytes	BYTE 80h,66h,0A5h
	
.code
	MOV AL,myBytes
	ADD AL,[myBytes+1]
	ADD AL,[myBytes+2]
```
  # Addition and Subtraction
  ## INC and DEC instructions
  1. Add/Subtract 1 from operand (register/memory)
  2. `INC` destination => (e.g destination++)
  3. `DEC` destination => (e.g destination--)
```txt
.data
	myWord WORD 	1000h
	myDword DWORD	10000000h

.code
	INC myWord		; 1001h
	DEC myWord		; 1000h
	INC myDword		; 10000001h
	
	MOV AX,00FFh
	INC AX			; AX = 0100h
	MOV AX,00FFh
	INC AL			; AX = 0000h
```
## ADD and SUB instructions
1. `ADD` destination, source
2. `SUB` destination, source
> **NOTE:** Same operand rules as for the MOV instructions.
```txt
.data
	var1 DWORD 10000h
	var2 DWORD 20000h

.code
	MOV EAX,var1		; 00010000h
	ADD EAX,var2		; 00030000h
	ADD AX,0FFFFh		; 0003FFFFh
	ADD EAX,1			; 00040000h
	SUB AX,1			; 0004FFFFh
```
## NEG (negate) instruction
- Reverses the sign of an operand in a register/memory location (*2nd complement*).
```txt
.data
	valB BYTE -1
	valW WORD +32767

.code
	MOV AL,valB		; AL = -1
	NEG AL			; AL = +1
	NEG valW		; valW = -32767 (Cannot do the reverse)
```
![arithmeticinHLL.png](../assets/Reverse%20Engineering/arithmeticinHLL.png)

---
# Data related operators and directives
## Align directive
- The `ALIGN` directive aligns a variable on a byte, word, doubleword, or a paragraph boundary:
```txt
.data
	bVal	BYTE ?	; 00404000
	ALIGN 2
	wVal	WORD ?	; 00404002
	bVal	BYTE ?	; 00404004
	ALIGN 4
	dVal	DWORD ?	; 00404008
	dVal	DWORD ?	; 0040400c
```
## PTR operator 
- Overrides the default type of a label (Variable)
- Provides the flexibility to access part of a variable.
- Requires a prefixed size specifier

```txt
.data 
	myDouble DWORD	12345678h
	
.code
	MOV AX,myDouble				; error! word<-dword
	MOV AX,WORD PTR myDouble	; loads 5678h
	MOV WORD PTR myDouble,4321h	; saves 4321h
```
- **Little Endian order (revise)**

![littleEndian.png](../assets/Reverse%20Engineering/littleEndian.png)

- **PTR example**

![PTRexample.png](../assets/Reverse%20Engineering/PTRexample.png)

- **Combine elements of a smaller data type into a larger operand**
> The CPU will automatically reverse the bytes

```txt
.data
	myBytes	BYTE 12h. 34h, 56h, 78h
	
.code
	MOV AX,WORD PTR [myBytes]	; AX = 3412h
	MOV AX,WORD PTR [myBytes+2]	; AX = 7856h
	MOV AX,DWORD PTR myBytes	; EAX = 78563421h
```
- **More examples**
```txt
.data
	varB BYTE 65h, 31h, 02h, 05h
	varW WORD 6543h, 1202h
	varD DWORD 12345678h
	
.code
	MOV AX,WORD PTR [varB+2]	; AX=0502h
	MOV BL,BYTE PTR varD		; BL=78h
	MOV BL,BYTE PTR [varW+2]	; BL=02h
	MOV AX,WORD PTR [varD+2]	; AX=1234h
	MOV EAX,DWORD PTR varW		; EAX=12026543h
```

## TYPE operator
- Returns the ***size of a single element*** of a data declaration (in bytes).
```txt
.data
	var1 BYTE ?
	var2 WORD ?
	var3 DWORD ?
	var4 QWORD ?
	
.code
	MOV EAX, TYPE var1	; 1
	MOV EAX, TYPE var2	; 2
	MOV EAX, TYPE var3	; 4
	MOV EAX, TYPE var4	; 8
```
## LENGTHOF operator
- Counts the ***number of elements*** in a single data declaration
```txt
.data
	byte1		BYTE 10,20,30			; 3
	array1		WORD 30 DUP(?),0,0		; 32
	array2		WORD 5 DUP(3 DUP(?))	; 15
	array3		DWORD 1,2,3,4			; 4
	digitStr	BYTE "12345678",0		; 9

.code
	MOV ECX,LENGTHOF array1	;32
```
## SIZEOF operator
- Equivalent of multiplying **`SIZEOF =LENGTHOF * TYPE`**
```txt
.data
	byte1		BYTE 10,20,30			; 3
	array1		WORD 30 DUP(?),0,0		; 64
	array2		WORD 5 DUP(3 DUP(?))	; 30
	array3		DWORD 1,2,3,4			; 16
	digitStr	BYTE "12345678",0		; 9

.code
	MOV ECX,SIZEOF array1	; 64
```
## Multiple lines and anonymous data
- **Spanning multiple lines**
![spanningmultiplelines.png](../assets/Reverse%20Engineering/spanningmultiplelines.png)

- **Anonymous data**
![anonymousdata.png](../assets/Reverse%20Engineering/anonymousdata.png)

## LABEL directive
- Assigns an alternate label name and type to an existing storage location.
- Does ***not allocate any storage*** of it's own.
- Avoids the need for the PTR operator.
```txt
.data
	dwList		LABEL	DWORD
	wordList	LABEL	WORD
	byteList	BYTE	00h,10h,00h,20h

.code
	MOV EAX,dwList		; 20001000h
	MOV CX,wordList		; 1000h
	MOV DL,intList		; 00h
```
> **`dwList`**, **`wordList`**, **`intList`** are the same offset  (address).

## OFFSET operator
Used for ***indirect addressing***
- **`OFFSET`** returns the distance in bytes of a label from the beginning of it's enclosing segment.
- **`Protected mode`**: 32 bits
- **`Real mode`**: 16 bits

![offsetpic.png](../assets/Reverse%20Engineering/offsetpic.png)
- **Example**: 
Assume that **`bVal`** is located at offset **`0040400h`**
```txt
.data
	bVal BYTE	?
	wVal WORD	?
	dVal DWORD	?
	dVal2 DWORD	?
	
.code
	MOV ESI, OFFSET bVal	; ESI = 00404000
	MOV ESI, OFFSET wVal	; ESI = 00404001
	MOV ESI, OFFSET dVal	; ESI = 00404003
	MOV ESI, OFFSET dVal2	; ESI = 00404007
```
- **Another example**
```txt
.data
	varB BYTE	65h, 31h, 02h, 05h
	varW WORD	6543h, 1202h
	varD DWORD	12345678h
	
.code
	MOV AX, WORD PTR [varB+2]	; AX=0502h
	MOV BL, BYTE PTR varD		; BL=78h
	MOV BL, BYTE PTR [varW+2]	; BL=02h
	MOV AX, WORD PTR [varD+2]	; AX=1234h
	MOV EAX, DWORD PTR varW
	
```
## ESI register
Is an indirect operand (Register as a pointer).
- It holds the address of a variable, usually an array or a string.
- It can be de-referenced (just like a pointer) using **`[ESI]`**.
- Works with **`OFFSET`** to produce the address to de-reference.
```txt
.data
	val1 BYTE 10h, 20h, 30h

.code
	MOV ESI, OFFSET val1	; ESI stores address of val1 
	MOV AL, [ESI]			; dereference ESI (AL = 10h)
	INC ESI
	MOV AL, [ESI]			; AL = 20h
	INC ESI
	MOV AL, [ESI]			; AL = 30h
```
### PTR for indirect addressing
- Use it to clarify the size attribute of a memory operand
- When we have an address (offset) we don't know the size of the values at that offset and must specify them explicitly.
```txt
.data
	myCount WORD 0
	
.code
	MOV ESI, OFFSET myCount
	
	INC [ESI]				; Error: Operand must have size
	INC WORD PTR [ESI]		; OK
	
	ADD [ESI], 20			; Error...
	ADD WORD PTR [ESI], 20 	; OK
```
## Indirect operand (variable as a pointer)
- Offsets are of size **`DWORD`**.
- A variable if size **`DWORD`** can hold an offset.
- i.e you can declare a pointer variable that contains the offset of another variable.
```txt
.data
	arrayW 	WORD	1000h,2000h,3000h
	ptrW	DWORD	arrayW			; ptrW = offset of arrayW
	ptrW	DWORD	OFFSET arrayW 	; Same as above
	
.code
	MOV ESI, ptrW
	MOV AX, [ESI]	; AX = 1000h
```
## Array sum example
- Indirect operands are ideal for traversing an array.
> **`NOTE`** : The register in brackets must be incremented by a value that matches the array type (i.e 2 for WORD, 4 for DWORD, 8 for QWORD).
```txt
.data
	arrayW WORD 1000h, 2000h, 3000h
	
.code
	MOV ESI, OFFSET	arrayW
	MOV AX, [ESI]
	ADD ESI, 2
	;or add esi,TYPE arrayW  ; good clarity
	ADD AX, [ESI]
	ADD ESI, 2
	ADD AX, [ESI]	; AX = sum of the array
```
## JMP instructions
- Jumps are the basics of most control flow.
- HLL compilers turn loops, if statements, switches etc. into same kind of jump.
- JMP is an **`unconditional jump`** to a label that is usually within the same procedure.
- Syntax: JMP target
- Logic:**`EIP <- target`**

> A jump outside the current procedure must be to a special type of label called a **`global`** label.
## LOOP instruction
- It creates a `Counted loop` using **`ECX`**
- Syntax: LOOP target
- Target should precede the instruction
	- **`ECX`** must contain the iteration count.
- Logic:
	- **`ECX <- ECX -1`**
	- If **`ECX !=0`** , jump back to target, else go to the next instruction. 
```txt
.code
	MOV AX, 0
	MOV ECX, 5
L1:
	ADD AX, CX
	LOOP L1
;This loop calculates the sum:  5+4+3+2+1
```
---
# References
1. [Brief Introduction to NASM](%20https%3A//montcs.bloomu.edu/Information/LowLevel/Assembly/assembly-tutorial.html)
2. [Nasm tutorial](https://cs.lmu.edu/~ray/notes/nasmtutorial/)*