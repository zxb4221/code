package main

import (
    "fmt"
    "log"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)

func main() {
    


    db, err := sql.Open("mysql","sysbench:123456@tcp(10.37.163.58:3306)/sysbench")
    
    if err != nil{
        fmt.Println("sql.Open error")
        return
    }
    
    defer db.Close()
    
    
    selectDB(db)   
    
    insertDB(db)

    updateDB(db)
    
    deleteDB(db)
}

func selectDB(db *sql.DB){

   rows, err := db.Query("SELECT id,k,c,pad FROM sbtest1 limit 5")
   defer rows.Close()
   if err != nil {
      log.Println(err)
      return
   }

   for rows.Next() {

      var id int
      var k int
      var c string
      var pad string

      rows.Columns()
      err = rows.Scan(&id, &k, &c, &pad)
      fmt.Printf("id:%d,k:%d,c:%s,pad:%s\n",id,k,c,pad)
   }

}

func insertDB(db *sql.DB){

   stmt, err := db.Prepare("INSERT INTO sbtest1(k,c,pad) VALUES(?, ?, ?)")
   defer stmt.Close()

   if err != nil {
      log.Println(err)
      return
   }
   stmt.Exec(100, "100", "100")
   stmt.Exec(200, "200", "200")
}


func updateDB(db *sql.DB)  {

   stmt, err := db.Prepare("UPDATE sbtest1 SET c=?,pad=? WHERE k=?")

   defer stmt.Close()
   if err != nil{
      log.Print(err)
      return
   }
   res, err := stmt.Exec("1000", "1000", 100)

   num, err := res.RowsAffected()

   fmt.Println(num)

}

func deleteDB(db *sql.DB){

   stmt, err := db.Prepare("DELETE FROM sbtest1 WHERE k=?")
   defer stmt.Close()

   if err != nil{
      log.Print(err)
      return
   }
   res, err := stmt.Exec(200)

   num, err := res.RowsAffected()

   fmt.Println(num)

}


