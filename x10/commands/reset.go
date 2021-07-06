package commands

import (
	"os"

	"m0rg.dev/x10/plumbing"
	"m0rg.dev/x10/x10_log"
)

type ResetCommand struct{}

func init() {
	RegisterCommand("reset", ResetCommand{})
}

func (cmd ResetCommand) Run(args []string) {
	logger := x10_log.Get("main")

	target := os.Args[2]
	plumbing.Reset(logger, target)
}
