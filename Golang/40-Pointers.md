# Pointers
---
## Basic Syntax
```go
package main

import "fmt"

func main() {
	var a int = 42
	var b *int = &a //Points to "a" address.
	fmt.Println(&a,b)
}
```
## Derefrencing
```go
package main

import "fmt"

func main() {
	var a int = 42
	var b *int = &a //Points to "a" address.
	fmt.Println(a,*b) // Makes the complier find the value stored in memmory annd displayes it.
}
```
**Examples**
```go
package main

import "fmt"

func main() {
	var a int = 42
	var b *int = &a //Points to "a" address.
	*b = 15
	fmt.Println(a,*b) //Prints 15
}
```

```go
package main

import "fmt"

func main() {
	a := [3]int{1,2,3}
	b := &a[0]
	c := &a[1]
	fmt.Printf("%v %p %p\n",a,b,c)
}
```
**Pointers arthmetic isn't available in go**
The following code will produce an error:
```go
package main

import "fmt"

func main() {
	a := [3]int{1,2,3}
	b := &a[0]
	c := &a[1] - 4
	fmt.Printf("%v %p %p\n",a,b,c)
}
```
> Note: You can use `unsafe` package

## Pointers with structs
The output is like saying: "`ms` is holding the address of an object that has a field of `value 42` in it "
```go
package main

import "fmt"

func main() {
	var ms *myStruct
	ms = &myStruct{foo:42}
	fmt.Println(ms)
}

type myStruct struct{
	foo int
}
```
**With an empty object**
```go
package main

import "fmt"

func main() {
	var ms *myStruct
	ms = new(myStruct)
	fmt.Println(ms)
}

type myStruct struct{
	foo int
}
```
## *nil*
```go
package main

import "fmt"

func main() {
	var ms *myStruct
	fmt.Println(ms) // Because the ms Points to Null
	ms = &myStruct{foo:42}
	fmt.Println(ms)
}

type myStruct struct{
	foo int
}
```
**Assigning a value**
```go
package main

import "fmt"

func main() {
	var ms *myStruct
	ms = new(myStruct)
	(*ms).foo = 42
	fmt.Println((*ms).foo)
}

type myStruct struct{
	foo int
}
```
**Compiler can help us :)**
```go
package main

import "fmt"

func main() {
	var ms *myStruct
	ms = new(myStruct)
	ms.foo = 42
	fmt.Println(ms.foo)
}

type myStruct struct{
	foo int
}
```


