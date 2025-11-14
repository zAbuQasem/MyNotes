## Basic Syntax
```go
package main

import (
	"fmt"
)

func main() {
	grades := [3]int{97,55,44}
	fmt.Printf("Grades: %v",grades)
}
```
## Array without a specific size
```go
//Added [...] instead of [<NUMBER>]
package main

import (
	"fmt"
)

func main() {
	grades := [...]int{97,55,44,84,979,111}
	fmt.Printf("Grades: %v",grades)
}
```

## Empty array with a specific size
```go
package main

import (
	"fmt"
)

func main() {
	var students [3]string
	fmt.Printf("Students: %v\n",students) //Empty
	students[0] = "AbuQasem"
	students[1] = "Omar"
	fmt.Printf("Students: %v\n",students) //Two elements
	fmt.Printf("Student #1 %v\n",students[1]) // Specific element
	fmt.Printf("No. of Students: %v\n",len(students)) //length of array
}
```
## Array holding arrays :smiley:
```go
package main

import (
	"fmt"
)

func main() {
	var identityMatrix [3][3]int = [3][3]int{ [3]int{1,0,0},[3]int{0,1,0}, [3]int{0,1,1} }
	fmt.Println(identityMatrix)
}
```
## Array holding arrays without banging your head against the wall :smile:
```go
package main

import (
	"fmt"
)

func main() {
	var identityMatrix [3][3]int
	identityMatrix[0] = [3]int{1,0,0}
	identityMatrix[1] = [3]int{0,1,0}
	identityMatrix[2] = [3]int{0,0,1}
	fmt.Println(identityMatrix)
}
```
## Copying an array
```go
package main

import (
	"fmt"
)

func main() {
	a := [...]int{1,2,3}
	b := a  //Entire array is copied to 'b'
	b[1] = 5
	fmt.Println(a)
	fmt.Println(b)
}
```
## Copying a whole array to a variable isn't effifcient so we will use a pointer:
```go
package main

import (
	"fmt"
)

func main() {
	a := [...]int{1,2,3}
	b := &a
	b[1] = 5   //Changing the value here changes actually for both variables because they both point to the same array.
	fmt.Println(a)
	fmt.Println(b)

}
```
# Slices
## Anything you can do with an `array` you also can do it with a `slice`
```go
package main

import (
	"fmt"
)

func main() {
	a := []int{1,2,3}
	b := a
	b[1] = 5    // In a slice changing the value will change for all the underlying variables containing the array.
	fmt.Println(a)
	fmt.Println(b)
	fmt.Println(len(a))
	fmt.Println(cap(a))
}
```

## Slicing examples
```go
package main

import (
	"fmt"
)

func main() {
	a := []int{1,2,3,4,5,6,7,8,9,10}
	b := a[:]  //Slice all elements
	c := a[3:] //Slice from 4th element to end
	d := a[:6] //Slice from first to 6th element
	e := a[3:6] //Slice from the 4th till the 6th element
	fmt.Println(a)
	fmt.Println(b)
	fmt.Println(c)
	fmt.Println(d)
	fmt.Println(e)
}


```
## Another way for creating slices (efficient and i can control the capacity)
```go
package main

import (
	"fmt"
)

func main() {
	a := make([]int,0, 100) //no of elements is 0 & capacity is 100
	a = append(a,1,3) //added two elements
	fmt.Println(a)
	fmt.Printf("Length: %v\n",len(a))
	fmt.Printf("Capacity: %v\n",cap(a))
}
```

## Removing an element from the middle
```go
package main

import (
	"fmt"
)

func main() {
	a := []int{1,2,3,4,5}
	b := append(a[:2], a[3:]...) // 3 dots for concatination
	fmt.Println(b)
	//fmt.Println(a) //This will change the array of "a".
	
}
```

### Summary
![arrayssum](attachments/arrayssum.png)