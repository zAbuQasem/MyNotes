# Functions
---
## Basic Syntax
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello World!")
}
```
## Passing values through functions
```go
package main

import "fmt"

func main() {
    sayMessage("Hello World!")
}

func sayMessage(msg string){
    fmt.Println(msg)
}
```
**Examples**
```go
package main

import "fmt"

func main() {
    sayMessage("Hello World!", 1)
}

func sayMessage(msg string, num int){
    fmt.Println(msg,num)
}
```
## Functions with Pointers
```go
package main

import "fmt"

func main() {
    greeting := "Hello"
    name := "Omar"
    sayMessage(&greeting,&name)
    fmt.Println(name) // will print "khattab" because we changed it with a pointer in the sayMessage pointer  
}

func sayMessage(greeting *string, name *string){
    fmt.Println(*greeting,*name)
    *name = "Khattab"  // -> here
    fmt.Println(*name)
}
```