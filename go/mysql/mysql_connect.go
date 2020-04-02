package main

import (
    "fmt"
    "time"
    "log"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)

func main() {
    

    maxConnect := 300

    db, err := sql.Open("mysql","sysbench:123456@tcp(10.37.163.58:3306)/sysbench")
    if err != nil{
        fmt.Println("sql.Open error")
    }
    
    db.SetMaxOpenConns(maxConnect)
    //设置上数据库最大闲置连接数
    db.SetMaxIdleConns(maxConnect)
    

    stopC := make(chan int, maxConnect)
   
    for i := 0; i < maxConnect; i++ {
        go func(){
            _, err = db.Query("select 1")
            if err != nil {
                log.Fatal(err)
            }
            stopC <- 0
        }()
    }

    for i := 0; i < maxConnect; i++{
        <-stopC
    }
    fmt.Println("before sleep")
    time.Sleep(time.Duration(60)*time.Second)
    fmt.Println("end")


}
