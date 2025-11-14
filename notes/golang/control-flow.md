# Control Flow
---
## Navigation
- **[[#Defer]]**
- **[[#Panic]]**
- **[[#Recover]]**
## Defer
Delay the execution of the function or method or an anonymous method until the nearby functions returns.
 Defer is used to ensure that a function call is performed later in a program’s execution, usually for purposes of cleanup.
 **Not the best option when working with an enormous amount of resources.**
### Basic Syntax
```go
package main
import (
	"fmt"
)

func main() {
	fmt.Println("Start")
	defer fmt.Println("middle")
	fmt.Println("last")
}
```
**Example**
```go
package main

import (
    "fmt"
    "os"
)

func main() {

    f := createFile("/tmp/defer.txt")
    defer closeFile(f)
    writeFile(f)
}

func createFile(p string) *os.File {
    fmt.Println("creating")
    f, err := os.Create(p)
    if err != nil {
        panic(err)
    }
    return f
}

func writeFile(f *os.File) {
    fmt.Println("writing")
    fmt.Fprintln(f, "data")

}

func closeFile(f *os.File) {
    fmt.Println("closing")
    err := f.Close()

    if err != nil {
        fmt.Fprintf(os.Stderr, "error: %v\n", err)
        os.Exit(1)
    }
}
```
**Example**
```go
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	res, err := http.Get("http://www.gogle.com/robots.txt")
	if err !=nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	robots, err := ioutil.ReadAll(res.Body)
	if err !=nil {
		log.Fatal(err)
	}
	fmt.Printf("%s",robots)
}
```
## Panic
A `panic` typically means something went unexpectedly wrong. Mostly we use it to fail fast on errors that shouldn’t occur during normal operation, or that we aren’t prepared to handle gracefully.
Defers happen before a Panic
### Basic Syntax
```go
package main

import (
	"fmt"
)

func main() {
	fmt.Println("a")
	panic("A Problem has occured!")
	fmt.Println("b")
}
```
**Example**
```go
package main

import "os"

func main() {

    panic("a problem")

    _, err := os.Create("/tmp/file")
    if err != nil {
        panic(err)
    }
}
```
**Example**
```go
package main

import (
	"fmt"
)

func main() {
	fmt.Println("start")
	defer fmt.Println("This was deferred")
	panic("A Problem has occured!")
	fmt.Println("end")
}
```
## Recover
**defer** function is the only function that is called before the **panic**. So it makes sense to put the **recover** function in the **defer** function only. If the **recover** function is not within the defer function then it will not stop **panic**.
```go
package main

import "fmt"

func main() {

	a := []string{"a", "b"}
	checkAndPrint(a, 2)
	fmt.Println("Exiting normally")
}

func checkAndPrint(a []string, index int) {
	defer handleOutOfBounds()
	if index > (len(a) - 1) {
		panic("Out of bound access for slice")
	}
	fmt.Println(a[index])
}

func handleOutOfBounds() {
	if r := recover(); r != nil {
		fmt.Println("Recovering from panic:", r)
	}
}
```
> Explained the code above: https://golangbyexample.com/recover-example-go/