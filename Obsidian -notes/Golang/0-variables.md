```go
package main

import (
	"fmt"
)

func main() {
	var i int
	i = 42
	var j int = 27
	k := 99     //Leaving the declaration for the compiler
	fmt.Printf("%T %T %T",i,j,k)
}
```

```go
package main

import (
	"fmt"
)

var (   //initalizing variables at the package level.

	i int = 1337   //No need to put "var" before them.
	j  int = 31337
	k string = "Meow"
)

func main() {
	fmt.Printf("%T, %T, %T\n", i, j, k)
}
```
 ## Notes
  in go every variable you initialize have by default the value of 0 == false
  
 **Visibility**
 - Lower case first letter for the package scope.
 - Upper case flrst letter will export the variable globally.
 - No private scope.
 
 **Naming conventins**
 - Pascal or camelCase (Don't use underscore or a score).
 -- Capiltilize acrnyms (HTTP,URL).
 - As short as reasonable.
 --Longer names for longer lives.
 
 **Type coversions**
 - DestinationType(variable)
 - Use `strconv` package for strings
