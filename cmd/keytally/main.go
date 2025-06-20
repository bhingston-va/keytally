package keytally

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/bhingston-va/keytally/internal/counter"
	"github.com/micmonay/keyboard"
)

func Execute() {
	c := counter.New()
	const dataFile = "key_counts.json"
	_ = c.Load(dataFile)

	if err := keyboard.Open(); err != nil {
		panic(err)
	}
	defer keyboard.Close()

	// Handle exit cleanly
	go func() {
		sig := make(chan os.Signal, 1)
		signal.Notify(sig, os.Interrupt, syscall.SIGTERM)
		<-sig
		c.Save(dataFile)
		fmt.Println("\nExiting...")
		os.Exit(0)
	}()

	fmt.Println("Keytally is running. Press ESC to exit.")
	for {
		char, key, err := keyboard.GetKey()
		if err != nil {
			panic(err)
		}
		if key.String() == "ESC" {
			break
		}
		k := key.String()
		if k == "" {
			k = string(char)
		}
		c.Increment(k)
		_ = c.Save(dataFile)
	}
}
