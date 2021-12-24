# Ubuntu
Install mono-complete
```bash
sudo apt install mono-complete
```
Compile using
```bash
mcs -out:hello.exe hello.cs
```
Run
```bash
mono hello.exe
```
Decompile the executable file.
```bash
monodis --output=decompiled-hello.txt hello.exe
```