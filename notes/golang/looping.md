# Looping
---
## Basic Syntax
```go
package main

import (
	"fmt"
)

func main() {
	for i := 0; i < 5; i++ {
		fmt.Println(i)
	}
}
```
## Multiple for loops
Note: Cannot use `i++` for nested because it's not an expression in golang.
```go
package main

import (
	"fmt"
)

func main() {
	for i , j := 0,0; i < 5; i,j = i+1, j+1 {
		fmt.Println(i,j)
	}
}
```
## Messing with loops
```go
package main

import (
	"fmt"
)

func main() {
	for i := 0; i < 5; i++ {
		fmt.Println(i)
	}
	//fmt.Println(i) -> won't work because i is defined just for the loop
}

//To make i global for the code block
package main

import (
	"fmt"
)

func main() {
	i := 0
	for ; i < 5; i++ {
		fmt.Println(i)
	}
	fmt.Println(i)
}
```
## Do , While in Golang
```go
package main

import (
	"fmt"
)

func main() {
	i :=0
	for ;i < 5; {
		fmt.Println(i)
		i++
	}
	}

// Here you can give up Semi colons because in go if you put a semi colon you have to end with other one

package main

import (
	"fmt"
)

func main() {
	i :=0
	for i < 5 {  // HERE
		fmt.Println(i)
		i++
	}
	}

```
## Infinite for loop
```go
package main

import (
	"fmt"
)

func main() {
	i :=0
	for {
		fmt.Println(i)
		i++
		}
	}
	
//To break & continue

package main

import (
	"fmt"
)

func main() {
	i :=0
	for {
		fmt.Println(i)
		i++
		if i == 5 {
			break
		}else{
			fmt.Println("continue lol")
			continue
		}
	}
}
```
## Nested For loops
```go
package main

import (
	"fmt"
)

func main() {
	i ,j := 0 ,0
	for i <= 3 {
		i++
		for j <= 3 {
			fmt.Println(i*j)
			j++
		}

	}
}
```
## for loops with slices and maps
**Slices & Arrays **
```go
package main

import (
	"fmt"
)

func main() {
	s := []int{1,2,3}
	for key,value := range s {
		fmt.Println(key,value)
	}
}
```

**Maps**
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
	for key,value := range StatePopulations {
		fmt.Println(key,value)
	}
}
```

## for looping a string
```go
package main

import (
	"fmt"
)

func main() {
	s := "AbuQasem"
	for key ,value := range s {
		fmt.Println(key,string(value))  // Without the string it will print the ascii value
	}
}
```