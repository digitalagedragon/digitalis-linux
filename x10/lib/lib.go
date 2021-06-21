package lib

import (
	"fmt"
	"io/ioutil"

	"github.com/sirupsen/logrus"
	"gopkg.in/yaml.v2"
	"m0rg.dev/x10/spec"
)

func LoadPackage(pkgsrc string) spec.SpecLayer {
	pkg := spec.Spec{}

	// Load the package YAML
	logrus.Info("Loading package: ", pkgsrc)
	pkgraw, err := ioutil.ReadFile(pkgsrc)
	if err != nil {
		panic(err)
	}

	err = yaml.UnmarshalStrict(pkgraw, &pkg)
	if err != nil {
		panic(err)
	}

	// Load and apply the layers.
	composite := spec.SpecLayer{}

	layers := make([]spec.SpecLayer, len(pkg.Layers)+1)
	for idx, layer_name := range pkg.Layers {
		logrus.Debug("Loading layer: ", layer_name)
		layers[idx] = LoadPackage(fmt.Sprintf("pkgs/layers/%s.yml", layer_name))
	}

	layers = append(layers, *pkg.Package)

	for _, layer := range layers {
		// Meta: Take the last complete struct.
		if layer.Meta != nil {
			composite.Meta = layer.Meta
		}

		// Depends: Concatenate arrays.
		composite.Depends.HostBuild = append(composite.Depends.HostBuild, layer.Depends.HostBuild...)
		composite.Depends.Build = append(composite.Depends.Build, layer.Depends.Build...)
		composite.Depends.Test = append(composite.Depends.Test, layer.Depends.Test...)
		composite.Depends.Run = append(composite.Depends.Run, layer.Depends.Run...)

		// Sources: Concatenate.
		composite.Sources = append(composite.Sources, layer.Sources...)

		// Stages: Piece-wise overlay.
		if composite.Stages == nil {
			composite.Stages = make(map[string]*spec.SpecStage)
		}

		for name, stage := range layer.Stages {
			// Make sure we have an object.
			if _, ok := composite.Stages[name]; !ok {
				composite.Stages[name] = new(spec.SpecStage)
				composite.Stages[name].UseWorkdir = new(bool)
				*composite.Stages[name].UseWorkdir = false
			}

			// Append pre- and post- arrays. Note ordering.
			composite.Stages[name].PreScript = append(composite.Stages[name].PreScript, stage.PreScript...)
			composite.Stages[name].PostScript = append(stage.PostScript, composite.Stages[name].PostScript...)

			// And take the script directly if present.
			if stage.Script != nil {
				composite.Stages[name].Script = stage.Script
			}

			// UseWorkdir: Take last.
			if stage.UseWorkdir != nil {
				composite.Stages[name].UseWorkdir = stage.UseWorkdir
			}
		}

		// StageOrder: Take the last complete array.
		if layer.StageOrder != nil {
			composite.StageOrder = layer.StageOrder
		}

		// Environment: Overlay map contents.
		if composite.Environment == nil {
			composite.Environment = make(map[string]string)
		}

		for name, value := range layer.Environment {
			composite.Environment[name] = value
		}

		// Workdir: Take last.
		if len(layer.Workdir) > 0 {
			composite.Workdir = layer.Workdir
		}
	}

	return composite
}

func LoadLayer(layersrc string) spec.SpecLayer {
	layer := spec.SpecLayer{}

	pkgraw, err := ioutil.ReadFile(layersrc)
	if err != nil {
		panic(err)
	}

	err = yaml.UnmarshalStrict(pkgraw, &layer)
	if err != nil {
		panic(err)
	}

	return layer
}
