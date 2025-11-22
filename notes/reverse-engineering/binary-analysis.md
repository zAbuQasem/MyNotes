# Binary analysis
---
## Symbols and stripped binaries
## Symbolic information
High-level source code, such as C code, centers around functions and variables with meaningful, human-readable names. When compiling a program,compilers emit symbols, which keep track of such symbolic
names and record which binary code and data correspond to each symbol.
- Getting the main function address and size (bytes)
```bash
readelf --syms <Executable> | grep -i "main"
```
> **ELF binaries**, debugging symbols are typically generated in the DWARF format,5 while **PE binaries** usually use the proprietary...Microsoft Portable Debugging (PDB) format. DWARF information is usually embedded within the binary, while PDB comes in the form of a separate symbol file.
## Binary stripping
Unfortunately, extensive debugging information typically isn’t included
in production-ready binaries, and even basic symbolic information is often stripped to *reduce file sizes and prevent reverse engineering*, especially in the case of malware or proprietary software. This means that as a binary analyst, you often have to deal with the far more challenging case of stripped binaries without any form of symbolic information.
- Stripping a binary
```bash
strip --strip-all <Executable>
```
---
## Disassembling a binary
## Object files
- Disassembling an object file
```bash
#show the contents of the .rodata (read-only data) section
objdump -sj .rodata example.o

#disassembles in intel syntax 
objdump -M intel -d compilation_example.o
```
>**Data** and **code references** from object files are not yet fully resolved because the compiler doesn’t know at what base address the file will eventually be loaded. That's why the assembly code looks nonsensical.

You can confirm this by asking `readelf` to show you all the relocation symbols present in the object file.
```bash
readelf -relocs example.o
```
The relocation symbol tells the linker that it should resolve the reference to the string to point to whatever address it ends up at in the `.rodata` section.
## Complete binary executable
- Disassembling an executable with `objdump`
```bash
objdump -M intel -d <Executable>
```
> Although the different sections are clearly distinguishable in both stripped and non-stripped binaries, the stripped binary functions are not distinguishable.
---
## ELF format
**ELF binaries** really consist of only four types of components: an `executable header`, a series of (optional) `program headers`, a `number of sections`, and a series of (optional) `section headers`, one per section.
> You can find the definitions of ELF-related types and constants in `/usr/include/elf.h` .

![ELF-format](attachments/ELF-format.png)

## Executable header
Is just a structured series of bytes telling you that it’s an ELF file, what kind of ELF file it is, and where in the file to find all the other contents.
```c
/* The ELF file header. */
typedef struct
{
  unsigned char e_ident[EI_NIDENT];	/* Magic number and other info */
  Elf32_Half    e_type;	/* Object file type */
  Elf32_Half    e_machine;	/* Architecture */
  Elf32_Word    e_version;	/* Object file version */
  Elf32_Addr    e_entry;	/* Entry point virtual address */
  Elf32_Off     e_phoff;	/* Program header table file offset */
  Elf32_Off     e_shoff;	/* Section header table file offset */
  Elf32_Word    e_flags;	/* Processor-specific flags */
  Elf32_Half    e_ehsize;	/* ELF header size in bytes */
  Elf32_Half    e_phentsize;	/* Program header table entry size */
  Elf32_Half    e_phnum;	/* Program header table entry count */
  Elf32_Half    e_shentsize;	/* Section header table entry size */
  Elf32_Half    e_shnum;	/* Section header table entry count */
  Elf32_Half    e_shstrndx;	/* Section header string table index */
} Elf32_Ehdr;
```
- **To read the ELF header**
```bash
readelf -h <excutalbe>
```
> Those headers are explained in details in `Practical binary analysis` book  page [33] ...
> And  in this link => [https://refspecs.linuxbase.org/elf/elf.pdf](https://refspecs.linuxbase.org/elf/elf.pdf)

## Section header
The code and data in an ELF binary are logically divided into contiguous non overlapping chunks called sections.
1. Sections don’t have any predetermined structure.
2. Often a section is nothing more than an unstructured blob of code or data. Every section is described by a section header.
3. Some sections contain data that isn’t needed for execution at all, such as symbolic or relocation information.
4. sections are intended to provide a view for the linker only, the
section header table is an optional part of the ELF format. ELF files that don’t need linking aren’t required to have a section header table. If no section header table is present, the e_shoff field in the executable header is set to zero.
```c
/* Section header. */
typedef struct
{
  Elf64_Word    sh_name;	/* Section name (string tbl index) */
  Elf64_Word    sh_type;	/* Section type */
  Elf64_Xword   sh_flags;	/* Section flags */
  Elf64_Addr    sh_addr;	/* Section virtual addr at execution */
  Elf64_Off     sh_offset;	/* Section file offset */
  Elf64_Xword   sh_size;	/* Section size in bytes */
  Elf64_Word    sh_link;	/* Link to another section */
  Elf64_Word    sh_info;	/* Additional section information */
  Elf64_Xword   sh_addralign;	/* Section alignment */
  Elf64_Xword   sh_entsize;	/* Entry size if section holds table */
} Elf64_Shdr;
```
> **Good explanation video**: https://www.youtube.com/watch?v=nC1U1LJQL8o
- **To read the all sections of an ELF executable**
```bash 
readelf -S --wide <Executable>
```
### .init and .fini sections
The **`.init`** section contains executable code that performs initialization tasks and needs to run before any other code in
the binary is executed.The `.fini` section is analogous to the `.init` section, except that it runs after the main program completes, essentially functioning as a kind of destructor.

### .text section
Is where the main code of the program resides,so it will frequently be the main focus of your binary analysis or reverse engineering efforts.
, the .text section of a typical binary compiled by gcc contains a num-
ber of standard functions that perform initialization and finalization tasks, such as `_start`, `register_tm_clones`, and `frame_dummy`.
- **Disassembly of `_start` function**
```bash
objdump -M intel -d <executable>
```

### .bss, .data, and .rodata sections
Those are writable sections used to contain variable Because code sections are generally not writable.
> Modern versions of gcc and clang generally don’t mix code and data, but Visual Studio sometimes does.

- **`.rodata`** section, which stands for “read-only data,” is dedicated to storing constant values (Not writable section).
- **`.data`** default values of initialized variables are stored here.
- **`.bss`** section reserves space for uninitialized variables. The name historically stands for “block started by symbol,” referring to the reserving of blocks of memory for (symbolic) variables.

>Unlike **.rodata** and **.data**, which have type SHT_PROGBITS, the .bss section has type SHT_NOBITS. This is because .bss doesn’t occupy any bytes in the binary as it exists on disk—it’s simply a **directive to allocate a properly sized block of memory for uninitialized variables**when setting up an execution environment for the binary. Typically, variables that live in .bss are zero initialized, and the section is marked as writable.

### Lazy Binding and the .plt, .got, and .got.plt sections
#### Lazy Binding and the PLT
 **dynamic linker** is the part of an operating system that loads and links the shared libraries needed by an executable when it is executed  at run time(**Lazy binding**), by copying the content of libraries from persistent storage to RAM.
 - On Linux, lazy binding is the default behavior of the dynamic linker.
- Lazy binding in Linux ELF binaries is implemented with the help of two special sections, called the **Procedure Linkage Table** (.plt) and the **Global Offset Table** (.got)
 
 ![calling a shared library via plt](attachments/calling%20a%20shared%20library%20via%20plt.png)
 
 - Disassembly of a **`.plt`** section
```bash
objdump -M intel --section .plt -d <executable>
```

> **`.got`** is for references to data items, while **`.got.plt`** is dedicated to storing resolved addresses for library functions accessed via the PLT.
> Explained in details in page [46-47] in practical binary analysis book

### .dynamic
The **`.dynamic`** section functions as a “road map” for the operating system and dynamic linker when loading and setting up an ELF binary for execution.
```bash
readelf --dynamic <Executable>
```
> Tags of type `DT_NEEDED` inform the dynamic linker about dependencies of the executable.
> The `DT_VERNEED` and `DT_VERNEEDNUM` tags specify the starting address and number of entries of the version dependency table, which indicates the expected version of the various dependencies of the executable.

### .init_array and .fini_array
The **`.init_array`** section contains an array of pointers to functions to use as constructors. Each of these functions is called in turn when the binary is initialized, before *main* is called.
In gcc, you can mark functions in your C source files as constructors by decorating them with `__attribute__((constructor))`
- Example
```c
#include <stdio.h>

#define MESSAGE  "In main!\n"
       
void constructorDEMO() __attribute((constructor));
void destructorDEMO() __attribute((destructor));

void constructorDEMO(){
        printf("\t\t\tPrinted Before main!\n\n");
}

void destructorDEMO(){
        printf("\n\t\t\tPrinted after main! :)");
}

int main(int argc, char *argv[]) {
        printf(MESSAGE);
        return 0;
}
```
- Display `.init_array` section
```txt
objdump -d --section .init_array <Executable>
```
**`.fini_array`** contains pointers to destructors rather than constructors. The pointers contained in `.init_array` and `.fini_array` are easy to change, making them convenient places to insert hooks that add initialization or finalization code to the binary to modify its behavior.
> Binaries produced by older gcc versions may contain sections called `.ctors` and `.dtors` instead of .init_array and .fini_array.

### .shstrtab, .symtab, .strtab, .dynsym, and .dynstr
- **`.shstrtab`** section is simply an array of NULL-terminated strings that contain the names of all the sections in the binary. *It’s indexed by the section headers to allow tools like readelf to find out the names of the sections*.
- **`.symtab`** section contains a symbol table.
- **`.strtab`** section contains the actual strings containing the symbolic names.
- **`.dynsym`** and **`.dynstr`**sections are analogous to .symtab and .strtab, except that they contain symbols and strings needed for dynamic linking rather than static linking. Because the information in these sections is needed during dynamic linking, they cannot be stripped.

## Program headers
The program header table provides a segment view of the binary.The segment view is used by t*he operating system and dynamic linker when loading an ELF into a process for execution to locate the relevant code and data and decide what to load into virtual memory.*
```c
/* Program segment header. */
typedef struct
{
  Elf64_Word    p_type;			/* Segment type */
  Elf64_Word    p_flags;		/* Segment flags */
  Elf64_Off     p_offset;		/* Segment file offset */
  Elf64_Addr    p_vaddr;		/* Segment virtual address */
  Elf64_Addr    p_paddr;		/* Segment physical address */
  Elf64_Xword   p_filesz;		/* Segment size in file */
  Elf64_Xword   p_memsz;		/* Segment size in memory */
  Elf64_Xword   p_align;		/* Segment alignment */
} Elf64_Phdr;
```
- Typical program header
```bash
readelf --wide --segments <Executable>
```
### The p_type Field
The p_type field identifies the type of the segment.Important values for this field include **`PT_LOAD`**, **`PT_DYNAMIC`**, and **`PT_INTERP`**.
- **`PT_LOAD`**:  Are intended to be loaded into memory when setting up the process.
- **`PT_INTERP`**: Contains the `.interp` section, which provides the name of the interpreter that is to be used to load the binary.
- **`PT_DYNAMIC`**: Contains the .dynamic section, which tells the interpreter how to parse and prepare the binary for execution.
- **`PT_PHDR`** encompasses (يشمل) the program header table.

### The p_flags Field
The flags specify the runtime access permissions for the segment. Three important types of flags exist: **`PF_X`**, **`PF_W`**, and **`PF_R`** (Read-Write-Execute).

### The p_offset, p_vaddr, p_paddr, p_filesz, and p_memsz Fields
Those are analogous to the **`sh_offset`**, **`sh_addr`**, and **`sh_size`** fields in a section header.They specify the *file offset* at which the segment starts, the *virtual address* at which it is to be loaded, and the *file size* of the segment.
> On some systems, it’s possible to use the **`p_paddr`** field to specify at which address in physical memory to load the segment. On modern operating systems such as Linux, this field is unused and set to zero since they execute all binaries in virtual memory.

### The p_align Field
The p_align field is analogous to the **`sh_addralign`** field in a section header. It indicates the required memory alignment (in bytes) for the segment. Just as with **`sh_addralign`**, an alignment value of 0 or 1 indicates that no particular alignment is required. If**` p_align`** isn’t set to 0 or 1, *then its value must be a power of 2*, and**` p_vaddr`** must be equal to **`p_offset`**, modulo **`p_align`**.

---
## Basic binary analysis in linux
## Commands and utilities
- **`ldd`** -> To explore binary dependencies
```bash
ldd <Executable>

#Output example
	linux-vdso.so.1 (0x00007ffd463fd000)
	lib5ae9b7f.so => not found
	libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f435eb6b000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f435eb51000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f435e929000)
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f435e845000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f435ed98000)
```
- **`xxd`** -> To view the file in a hex format
```bash
xxd <File>
xxd -c 32 <File>	# Display 32 bytes in each line
xxd -b <File>		# Display in binary
```
- **`dd`** -> Can be used to copy specific bytes from a file
```bash
dd if=WeirdFile of=elf_headerq count=64 skip=52 bs=1
## if=<InputFile>
## of=<OutputFile>
## count=<NumberOfBytesToCopy>
## skip=<NumberOfBytesToSkip>
## bs=<ReadAndWriteNumberOfBytesAt-a-Time>
```
- **`nm`** -> lists symbols in a given binary, object file, or shared object. When given a binary, by default attempts to parse the static symbol table.
```bash
nm <File> --demangle
#In case of a stripped file use -D \
#to parse the dynamic symbol table instead of the static symbol table.
nm -D <File> --demangle
```
> **More information**: C++ allows functions to be overloaded, which means there may be multiple functions with the same name, as long as they have different signatures. To eliminate duplicate names, C++ compilers emit **`mangled`**(مشوهة) function names. *A mangled name is essentially a combination of the original function name and an encoding of the function parameters*. This way, each version of the function gets a unique name, and the linker has no problems disambiguating(واضح) the overloaded functions. Mangled names are relatively easy to demangle.

- **`c++flit`** -> Used to demangle function names
```bash
c++filt _Z8rc4_initP11rc4_state_tPhi
$Output
rc4_init(rc4_state_t*, unsigned char*, int)
```
- **`ltrace`**, **`strace`** -> show the system calls and library calls, respectively, executed by a binary.
```bash
strace -i -C <Executable>
ltrace -i -C <Executable>
## -i -> Print the instruction pointer at every call.
## -C -> Automatically demangle c++ function names.
## -p <PID> -> to attach a process.
```
- **`gdb`** -> Mainly used for dynamic analysis.
```bash
gdb <executable>
gdb -p <PID>  #To attach a process.
```
## Determine an ELF size by it's header
SIZE = **`e_shoff`** + (**`e_shnum`** × **`e_shentsize`**)
```txt
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
readelf: Error: Too many program headers - 0x7 - the file is not that big
  Type:                              DYN (Shared object file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x970
  Start of program headers:          64 (bytes into file)
  Start of section headers:          8568 (bytes into file)  ----------> #e_shoff
  Flags:                             0x0
  Size of this header:               64 (bytes) ----------> # e_shentsize
  Size of program headers:           56 (bytes)
  Number of program headers:         7
  Size of section headers:           64 (bytes)
  Number of section headers:         27 ----------> # e_shnum
  Section header string table index: 26
```

## References
- [Patching ELF header](https://blog.elfy.io/)
- [Online ELF parser and editor](https://elfy.io/)
- [Detailed LinuxProgramStartup](http://dbp-consulting.com/tutorials/debugging/linuxProgramStartup.html)