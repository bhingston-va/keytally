package counter

import (
	"encoding/json"
	"os"
)

func (c *Counter) Save(path string) error {
	c.mu.Lock()
	defer c.mu.Unlock()
	file, err := os.Create(path)
	if err != nil {
		return err
	}
	defer file.Close()
	return json.NewEncoder(file).Encode(c.Counts)
}

func (c *Counter) Load(path string) error {
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close()
	return json.NewDecoder(file).Decode(&c.Counts)
}
