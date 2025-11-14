# Constants

#### Overriding a constant
```go
package main

import (
	"fmt"
)

const a int16 = 27

func main() {
	const a int = 42  //This inner constant shadows the outer constant
	fmt.Printf("%v ,%T\n",a, a)
}

```
#### Adding a constant to a variable
```go
package main

import (
	"fmt"
)

func main() {
	const a = 42
	var b int = 27 
	fmt.Printf("%v ,%T\n",a + b, a + b)  //The result will be a variable
}
```

#### Adding two different data types
This works because the complier treats the value of `a`  which is 42 as an int16 (This works only with constants )
```go
package main

import (
	"fmt"
)

func main() {
	const a = 42
	var b int16 = 27 
	fmt.Printf("%v ,%T\n",a + b, a + b) // fmt.Printf("%v ,%T\n",42 + b, 42 + b)
}
```

