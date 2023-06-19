package main

import (
	"encoding/json"
	"fmt"
)

type Input struct {
	Name string `json:"name"`
}

type Output struct {
	Result  int `json:"result"`
	Latency int `json:"latency"`
}

func hash(input string) int {
	hash := 0

	for i := 0; i < len(input); i++ {
		hash = (hash << 5) - hash + int(input[i])
		hash &= hash
	}

	return hash
}

func main(params json.RawMessage) (interface{}, error) {
	// Parse input parameters
	var input Input
	err := json.Unmarshal(params, &input)
	if err != nil {
		return nil, fmt.Errorf("failed to parse input: %v", err)
	}

	// If a value for name is provided, use it else use a default
	name := "stranger"
	if input.Name != "" {
		name = input.Name
	}

	output := Output{
		Result:  hash(name),
		Latency: 1,
	}

	return output, nil
}
