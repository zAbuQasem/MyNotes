# Misc
---
## Understanding `_`
It is called the blank identifier. Meaning the value assigned to it should be discarded. Because Go compiler doesn't allow you to create a variable you won't use.

**Let's take this example:**
```go
package main

import (
	"fmt"
	"net"
)

func main() {
	_,err := net.Dial("tcp","www.chegg.com:80")
	if err == nil {
		fmt.Println("it works!")
	}
}

//Ouutput: it works!
```
**Now let's remove the** `_`
```go
package main

import (
	"fmt"
	"net"
)

func main() {
	err := net.Dial("tcp","www.chegg.com:80")
	if err == nil {
		fmt.Println("it works!")
	}
}

//Output: ./main.go:9:6: assignment mismatch: 1 variable but net.Dial returns 2 values
```
**Then we must assign 2 variables, s let's define a variable**
```go
package main

import (
	"fmt"
	"net"
)

func main() {
	abuqasem,err := net.Dial("tcp","www.chegg.com:80")
	if err == nil {
		fmt.Println("it works!")
	}
}

//Output: ./main.go:9:2: abuqasem declared but not used
```
**So to avoid this error we have 2 options:**
1: Use the variable
```go
package main

import (
	"fmt"
	"net"
)

func main() {
	abuqasem,err := net.Dial("tcp","www.chegg.com:80")
	if err == nil && abuqasem != nil {
		fmt.Println("it works!")
	}
}

//Output: it works!
```
2: Use the `_` and make the code cleaner
```go
package main

import (
	"fmt"
	"net"
)

func main() {
	_,err := net.Dial("tcp","www.chegg.com:80")
	if err == nil {
		fmt.Println("it works!")
	}
}

//Output: it works!
```