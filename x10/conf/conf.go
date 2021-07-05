package conf

import (
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

func get(key string, def string) string {
	from_env, ok := os.LookupEnv(strings.ToUpper("x10_" + key))
	if !ok {
		from_env = def
	}
	return from_env
}

func TargetDir() string {
	return get("targetdir", "../targetdir")
}

func HostDir() string {
	return get("hostdir", "../hostdir")
}

func PkgDb() string {
	rc := filepath.Join(HostDir(), "binpkgs", "pkgdb.yml")
	os.MkdirAll(filepath.Join(HostDir(), "binpkgs"), os.ModePerm)
	return rc
}

func PackageDir() string {
	return get("packagedir", "../pkgs")
}

func BaseDir() string {
	_, b, _, _ := runtime.Caller(0)
	basepath, _ := filepath.Abs(filepath.Join(filepath.Dir(b), "../.."))
	return basepath
}
