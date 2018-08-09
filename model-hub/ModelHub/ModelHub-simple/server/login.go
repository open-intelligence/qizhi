package main

import (
	"database/sql"
	"fmt"
	"html/template"
	"log"
	"net/http"
)

func print_err(err error) {
	if err != nil {
		log.Println(err)
	}
}

type UserData struct {
	name string
	pswd string
}

func renderHTML(w http.ResponseWriter, file string, data interface{}) {
	t, err := template.New(file).ParseFiles("views/" + file)
	print_err(err)
	t.Execute(w, data)
}

func writeData(userData *UserData) string {
	db, err := sql.Open("mysql", "./data.db")
	print_err(err)
	defer db.Close()

	db.Exec(`create table data (id integer not null primary key, name text, data string);`)

	var olddata string
	var sqlStmt string

	err = db.QueryRow("select data from data where name = ?", userData.name).Scan(&olddata)
	if err != nil {
		sqlStmt = "insert into data(data, name) values(?,?)"
	} else {
		sqlStmt = "update data set data = ? where name == ?"
		if len(userData.pswd) == 0 {
			sqlStmt = "delete from data where data >= ? and name == ?"
		} else {
			userData.pswd = olddata + "\n" + userData.pswd
		}
	}

	stmt, err := db.Prepare(sqlStmt)
	print_err(err)
	defer stmt.Close()

	_, err = stmt.Exec(userData.pswd, userData.name)
	print_err(err)
	return userData.pswd
}

func index(w http.ResponseWriter, r *http.Request) {
	renderHTML(w, "index.html", "no data")
}

func login(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		err := r.ParseForm()

		if err != nil {
			fmt.Println("test1")
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}

		u := UserData{}
		u.name = r.Form.Get("username")
		u.pswd = r.Form.Get("usertext")

		u.pswd = writeData(&u)

		renderHTML(w, "page.html", u)
	} else {
		renderHTML(w, "redirect.html", "/")
	}
}
