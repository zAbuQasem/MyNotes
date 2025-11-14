# Concurrency (Go-routines)
---
## Basic Syntax
```go
package main

import (
	"fmt"
	"time"
)

func main() {
	meow := "Hello abuqasem!"
	go func(meow string){ //Passing the values is important to avoid race conditions and getting unwanted results
		fmt.Println(meow)
	}(meow)
	meow = "Bye!"
	time.Sleep(10 * time.Millisecond) //To give time to the print statement to work.
}

```
## Port scanner example
```go
package main

import (
	"fmt"
	"net"
	"time"
)

func main() {
	for i := 0; i <= 1024; i++ {
		time.Sleep(100 * time.Millisecond)
		go func(i int) {
			address := fmt.Sprintf("scanme.nmap.org:%d", i)
			conn, err := net.Dial("tcp", address)
			if err != nil {
				return
			}
			conn.Close()
			fmt.Println("[+]Port -> ", i)
		}(i)
	}
}

```
## Wait Groups
```go
package main

import (
	"fmt"
	"net"
	"sync"
)

func main() {
	var wg = sync.WaitGroup{}
	for i := 0; i <= 1024; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			address := fmt.Sprintf("scanme.nmap.org:%d", i)
			conn, err := net.Dial("tcp", address)
			if err != nil {
				return
			}
			conn.Close()
			fmt.Println("[+]Port -> ", i)
		}(i)
	}
	wg.Wait()
}

```

## Identifying race conditions
```bash
go run -race main.go
```