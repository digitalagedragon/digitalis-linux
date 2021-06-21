package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/sirupsen/logrus"
	"m0rg.dev/x10/lib"
)

func main() {
	if _, ok := os.LookupEnv("X10_DEBUG"); ok {
		logrus.SetLevel(logrus.DebugLevel)
	}
	buildCmd := flag.NewFlagSet("build", flag.ExitOnError)
	buildStage := buildCmd.String("stage", "", "Run only a specific stage.")

	if len(os.Args) < 2 {
		fmt.Printf("Usage: %s <subcommand> ...\n", os.Args[0])
		os.Exit(1)
	}

	switch os.Args[1] {
	case "gensum":
		pkgsrc := os.Args[2]
		pkg := lib.LoadPackage(pkgsrc)

		pkg.RunStage("fetch")
		pkg.RunStage("_gensum")
	case "build":
		buildCmd.Parse(os.Args[2:])
		pkgsrc := buildCmd.Arg(0)
		pkg := lib.LoadPackage(pkgsrc)

		if len(*buildStage) > 0 {
			err := pkg.RunStage(*buildStage)
			if err != nil {
				panic(err)
			}
		} else {
			for _, stage := range *pkg.StageOrder {
				err := pkg.RunStage(stage)
				if err != nil {
					panic(err)
				}
			}
		}
	}
}
