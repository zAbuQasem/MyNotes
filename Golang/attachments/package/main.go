package main

import (
	"fmt"
	"package/calculator"
	"package/greeter"
)

func main() {
	fmt.Println("=== Better Go Example ===")

	// Demonstrate the greeter package
	greeter.SayHello("World")
	greeter.SayHello("Go Developer")

	// Demonstrate the calculator package
	fmt.Println("\n=== Calculator Demo ===")
	a, b := 10, 5

	fmt.Printf("Adding %d + %d = %d\n", a, b, calculator.Add(a, b))
	fmt.Printf("Subtracting %d - %d = %d\n", a, b, calculator.Subtract(a, b))
	fmt.Printf("Multiplying %d * %d = %d\n", a, b, calculator.Multiply(a, b))

	result, err := calculator.Divide(a, b)
	if err != nil {
		fmt.Printf("Error dividing: %v\n", err)
	} else {
		fmt.Printf("Dividing %d / %d = %.2f\n", a, b, result)
	}

	// Test division by zero
	_, err = calculator.Divide(a, 0)
	if err != nil {
		fmt.Printf("Division by zero error: %v\n", err)
	}
}
