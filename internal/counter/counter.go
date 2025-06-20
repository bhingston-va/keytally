package counter

import "sync"

type Counter struct {
	mu     sync.Mutex
	Counts map[string]int
}

func New() *Counter {
	return &Counter{Counts: make(map[string]int)}
}

func (c *Counter) Increment(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.Counts[key]++
}
