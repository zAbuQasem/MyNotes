```go
package main

import (
	"fmt"
)

func main() {
	var n bool = true
	fmt.Printf("%v, %T\n", n,n)
}
```

```go
package main

import (
	"fmt"
)

func main() {
	n := 1 == 1
	m := 1 == 2
	fmt.Printf("%v, %T\n", n,n)
	fmt.Printf("%v, %T\n", m,m)
}
```

```go
package main

import (
	"fmt"
)

func main() {
	a := 10 // 1010
	b := 3  // 0011
	fmt.Println(a & b)  // 0010
	fmt.Println(a | b)  // 1011
	fmt.Println(a ^ b)  // 1001    //Exclusive OR
	fmt.Println(a &^ b) // 1000    // AND NOT
}
```

```go
package main

import (
	"fmt"
)

func main() {
	a := 8
	fmt.Println(a << 3) // 2^3 * 2^3 = 2^6 = 64
	fmt.Println(a >> 3) // 2^3 / 2^3 = 2^0 = 1
}
```

```go
package main

import (
	"fmt"
)

func main() {
	n := 3.14 // The compiler knew its a float
	n = 13.7e72 // Now n is known as a float  accros this block.
	n = 2.1E14
	fmt.Printf("%v, %T\n",n ,n)
}
```

```go
//Converting a string to asci
package main

import (
	"fmt"
)

func main() {
	s := "this is a string"
	b := []byte(s)
	fmt.Printf("%v ,%T\n",b,b)
}
```

