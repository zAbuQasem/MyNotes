package calculator

import (
	"errors"
	"fmt"
)

// Add returns the sum of two integers
func Add(a, b int) int {
	return a + b
}

// Subtract returns the difference of two integers
func Subtract(a, b int) int {
	return a - b
}

// Multiply returns the product of two integers
func Multiply(a, b int) int {
	return a * b
}

// Divide returns the quotient of two integers with error handling
func Divide(a, b int) (float64, error) {
	if b == 0 {
		return 0, errors.New("division by zero is not allowed")
	}
	return float64(a) / float64(b), nil
}

// Power returns a raised to the power of b
func Power(a, b int) int {
	if b == 0 {
		return 1
	}

	result := 1
	for i := 0; i < b; i++ {
		result *= a
	}
	return result
}

// PrintCalculation prints a formatted calculation result
func PrintCalculation(operation string, a, b int, result interface{}) {
	fmt.Printf("Operation: %s(%d, %d) = %v\n", operation, a, b, result)
}
