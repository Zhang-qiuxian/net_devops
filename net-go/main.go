package main

import (
	"net-go/router"
)

func main() {

	r := router.SetupRouter()
	r.Run()
}
