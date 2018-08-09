package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path"
)

func main() {
	fmt.Println("hello world")
	http.HandleFunc("/upload", uploadHandler)
	http.HandleFunc("/login", login)
	http.Handle("/", http.FileServer(http.Dir("test/")))
	http.ListenAndServe(":8080", nil)
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Method: ", r.Method)

	if r.Method == "POST" {
		err := r.ParseMultipartForm(32 << 20)
		if err != nil {
			fmt.Println("test1")
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}

		file, handler, err := r.FormFile("uploadfile")
		if err != nil {
			fmt.Println("test2")
			fmt.Println(err)
			return
		}
		defer file.Close()
		fmt.Fprintf(w, "%v", handler.Header)

		fmt.Println("dst: test/", handler.Filename)

		os.MkdirAll("test/"+path.Dir(handler.Filename), 0777)

		f, err := os.Create("test/" + handler.Filename)

		if err != nil {
			fmt.Println(err)
			return
		}
		defer f.Close()
		io.Copy(f, file)
	}

}
