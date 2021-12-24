# Channels
---
## Basic syntax
```go
package main

import (
	"fmt"
	"sync"
)

var wg = sync.WaitGroup{}

func main() {
	num := 0
	channel := make(chan int)
	for i := 0; i < 20; i++ {
		wg.Add(2)
		num ++
		go func() {
			defer wg.Done()
			channel <- num //Entering num value to the channel
		}()
		go func() {
			defer wg.Done()
			output := <-channel //Taking it from the channel to the output variable
			fmt.Println(output)
		}()
		wg.Wait()
	}
}
```

## Buffered channels to deal with data
```go
package main

import (
	"fmt"
	"sync"
)

var wg = sync.WaitGroup{}

func main() {
	num := 0
	num2 := 400
	channel := make(chan int, 100) //Store 100 integers
	for i := 0; i < 20; i++ {
		wg.Add(2)
		num ++
		go func() {
			defer wg.Done()
			channel <- num
			channel <- num2
		}()
		go func() {
			defer wg.Done()
			output := <-channel
			fmt.Println(output)
		}()
		wg.Wait()
	}
}
// If i did't specify a buufer this code will fail.
```
## Assigning a channel for sending and a channel for recieving
```go
package main

import (
	"fmt"
	"sync"
)

var wg = sync.WaitGroup{}

func main() {
	num := 0
	num2 := 400
	channel := make(chan int, 100) //Store 100 integers
	for i := 0; i < 20; i++ {
		wg.Add(2)
		num ++
		go func(channel chan <-  int ) { //Sender
			defer wg.Done()
			channel <- num
			channel <- num2
		}(channel)
		go func(channel <- chan int) { //receiver
			defer wg.Done()
			output := <- channel
			fmt.Println(output)
		}(channel)
		wg.Wait()
	}
}

```
**Better code to handle the situation
```go
package main

import (
	"fmt"
	"sync"
)

var wg = sync.WaitGroup{}

func main() {
	num := 0
	num2 := 100
	channel := make(chan int, 100) //Store 100 integers
		wg.Add(2)
		num ++

		//Receiver
		go func(channel chan <-  int ) {
			defer wg.Done()
			channel <- num
			channel <- num2
			close(channel)
		}(channel)
		

		//Sender
		go func(channel <- chan int) {
			defer wg.Done()
			for i := range channel {
				fmt.Println(i)
			}
		}(channel)
		wg.Wait()
	}
```