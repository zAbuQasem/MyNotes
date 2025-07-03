package greeter

import (
	"fmt"
	"time"
)

// SayHello prints a personalized greeting message
func SayHello(name string) {
	currentTime := time.Now()
	hour := currentTime.Hour()
	
	var greeting string
	switch {
	case hour < 12:
		greeting = "Good morning"
	case hour < 17:
		greeting = "Good afternoon"
	default:
		greeting = "Good evening"
	}
	
	fmt.Printf("%s, %s! 👋\n", greeting, name)
}

// GetWelcomeMessage returns a welcome message with current time
func GetWelcomeMessage(name string) string {
	return fmt.Sprintf("Welcome %s! Current time: %s", name, time.Now().Format("15:04:05"))
}
