package main

import (
	"fmt"
	"log"
	"os"
	"time"
)

type AgentLog struct {
	loger *log.Logger
	logFile *os.File
}

func (al *AgentLog) Info(info string) {
	timestamp := time.Now().Unix()
	tm := time.Unix(timestamp, 0)
	timeString := tm.Format("2006-01-02 15:04:05")

	al.loger.SetPrefix("[INFO][" + timeString + "]")
	al.loger.Println(info)
}


func NewLoger(fileName string) AgentLog {
	logFile, err  := os.OpenFile(fileName,os.O_RDWR|os.O_CREATE|os.O_APPEND,0644)
	if err != nil {
		fmt.Printf("open file error")
	}

	al := &AgentLog{}
	al.logFile = logFile
	al.loger = log.New(al.logFile,"[Info]",log.Llongfile)
	al.loger.SetPrefix("[Debug]")

	return *al
}

func (al *AgentLog) Close() {
	if al.logFile != nil{
		al.logFile.Close()
	}
}
