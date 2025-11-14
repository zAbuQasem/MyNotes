# If & Switch
## Basic Syntax
```go
package main

import (
	"fmt"
)

func main() {
	if true {
		fmt.Println("True :)")
	}

}
```

```go
package main

import (
	"fmt"
)

func main() {
	StatePopulations := make(map[string]int)
	StatePopulations = map[string]int{
		"Quds": 4518616,
		"Aleppo": 1812649,
		"Afghanistan": 2848284,
		"Borma": 481949,
		"Pakistan": 8418455,
		"Yemen": 841488,
	}
	if popul , ok := StatePopulations["Afghanistan"]; ok{
		fmt.Println(popul)
	}
}
```

```go
//Note: Position matters for else
package main

import (
	"fmt"
)

func main() {
	number := 50
	guess := 20
	if guess == number {
		fmt.Println("Correct")
		}else {
			fmt.Println("Wrong")
		}
}
```

## Switch
```go
package main

import (
	"fmt"
)

func main() {
	switch 5 {
	case 2,5,6:
		fmt.Println("Yes")
	default:
		fmt.Println("Nope")
		return
	}
}
```

```go
package main

import (
	"fmt"
)

func main() {
	switch i := 0+2; i {
	case 2:
		fmt.Println("Yes")
	default:
		fmt.Println("Nope")
		return
	}
}
```

```go
package main

import (
	"fmt"
)

func main() {
	i := 0+2
	switch {
	case i == 2 :
		fmt.Println("Yes")
	default:
		fmt.Println("Nope")
		return
	}
}
```