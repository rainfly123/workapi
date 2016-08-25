package main

import (
        "github.com/pili-engineering/pili-sdk-go/pili"
        "time"
        "strings"
        "sync"
        "fmt"
)
import "database/sql"
import _ "github.com/go-sql-driver/mysql"
import "net/http"
import "io"

const (
    ACCESS_KEY = "_x8qeD4FD5BGveRZ3SC_2_7StAUl_T7O9Sxz-e9X"
    SECRET_KEY = "mIEuQoIsUHw5eEgMhESAoDmQDXiw7tQVApcKue-E"
    HUB_NAME   = "66boss" 
    PUBLISH_KEY = "7cf0e739-8f53-4264-bea2-72aee33218e7"
)

var chans map[string]int64;
var mutex sync.Mutex

func getMysqlState(liveid string) int {
    db, err := sql.Open("mysql", "root:123321@/live")
    if err != nil {
        panic(err.Error()) 
    }
    defer db.Close()
    sql := fmt.Sprintf("select state from live where liveid=\"%s\" ", liveid)
    rows, err := db.Query(sql)
    var state int;
    if err == nil {
       for rows.Next() {
          rows.Scan(&state)
       }
    }
    return state;
}

func updateMysqlSnapshot(liveid string, snapshot string) {
    db, err := sql.Open("mysql", "root:123321@/live")
    if err != nil {
        panic(err.Error()) 
    }
    defer db.Close()

    // Prepare statement for inserting data
    stmtIns, err := db.Prepare("update live set snapshot=? where liveid=?") // ? = placeholder
    if err != nil {
        panic(err.Error()) 
    }
    defer stmtIns.Close() // Close the statement when we leave main() / the program terminates

    _, err = stmtIns.Exec(snapshot, liveid)
    if err != nil {
         panic(err.Error()) // proper error handling instead of panic in your app
    }
}


func updateMysqlState(liveid string, state int) {
    db, err := sql.Open("mysql", "root:123321@/live")
    if err != nil {
        panic(err.Error()) 
    }
    defer db.Close()

    // Prepare statement for inserting data
    stmtIns, err := db.Prepare("update live set state=? where liveid=?") // ? = placeholder
    if err != nil {
        panic(err.Error()) 
    }
    defer stmtIns.Close() // Close the statement when we leave main() / the program terminates

    _, err = stmtIns.Exec(state, liveid)
    if err != nil {
         panic(err.Error()) // proper error handling instead of panic in your app
    }
}

func updateMysqlPlayback(liveid string, url string) {
    db, err := sql.Open("mysql", "root:123321@/live")
    if err != nil {
        panic(err.Error()) 
    }
    defer db.Close()

    // Prepare statement for inserting data
    stmtIns, err := db.Prepare("update live set playback_hls_url=? where liveid=?") // ? = placeholder
    if err != nil {
        panic(err.Error()) 
    }
    defer stmtIns.Close() // Close the statement when we leave main() / the program terminates

    _, err = stmtIns.Exec(url, liveid)
    if err != nil {
         panic(err.Error()) // proper error handling instead of panic in your app
    }
}



func check_live_state(liveid string){

    credentials := pili.NewCredentials(ACCESS_KEY, SECRET_KEY)
    hub := pili.NewHub(credentials, HUB_NAME)
    stream, err := hub.GetStream(liveid)
    if err != nil {
        fmt.Println("Error:", err)
    }
    fmt.Println("GetStream:", stream)
    var start int64 
    //get status check if online
    var sleeped int32 = 0
    for {
        streamStatus, err := stream.Status()
        if err != nil {
          fmt.Println("Error:", err)
        }
        //fmt.Println("Stream Status:", streamStatus.Status)
        if strings.Contains(streamStatus.Status, "disconnect"){
          fmt.Printf("offline\n")
        }else {
            updateMysqlState(liveid, 1)  //living 
            start = time.Now().Unix()
            break
        }
        time.Sleep(time.Second * 10)
        sleeped += 1
        if sleeped >= 60480 {
            break
        }
    }
    mutex.Lock()
    chans[liveid] = start
    mutex.Unlock()

    offline  := 0
    for {
        //generate snapshot
        name := "snapshot.jpg" 
        format := "jpg"        
        options := pili.OptionalArguments{}
        snapshotRes, err := stream.Snapshot(name, format, options)
        if err != nil {
            fmt.Println("Error:", err)
        }
        fmt.Println("Stream Snapshot:\n", snapshotRes)
        //write mysql
        updateMysqlSnapshot(liveid, snapshotRes.TargetUrl)  //update snapshot
        time.Sleep(time.Second * 60)

        streamStatus, err := stream.Status()
        if err != nil {
          fmt.Println("Error:", err)
        }
        fmt.Println("Stream Status:", streamStatus.Status)
        if strings.Contains(streamStatus.Status, "disconnect"){
          fmt.Printf("offline\n")
          offline += 1
          if offline >= 2 {  //3minutes no stream
              break
          }
        }
    }

    //write mysql ,  stream  stopped 
    current := getMysqlState(liveid)
    if current == 2 {
        return
    }

    updateMysqlState(liveid, 2)  //stopped

    end := time.Now().Unix()
    name := "vod"             // required, string
    format := ""            // optional, string
    options:= pili.OptionalArguments{
        NotifyUrl: "",
        UserPipeline: "",
    } 

    saveAsRes, err := stream.SaveAs(name, format, int64(start), int64(end), options)
    if err != nil {
         fmt.Println("Error:", err)
    }
    fmt.Printf("SaveAs :%s\n", saveAsRes.Url)

    updateMysqlPlayback(liveid, saveAsRes.Url)
}

func receive_new_live(w http.ResponseWriter, req *http.Request) {
    io.WriteString(w, "hello, world!\n")
    if len(req.FormValue("liveid")) > 6 {
        go check_live_state(req.FormValue("liveid"))
    }
}

func stop_channel(w http.ResponseWriter, req *http.Request) {
    liveid := req.FormValue("liveid")
    if len(liveid) > 6 {

        credentials := pili.NewCredentials(ACCESS_KEY, SECRET_KEY)
        hub := pili.NewHub(credentials, HUB_NAME)
        stream, err := hub.GetStream(liveid)
        if err != nil {
            fmt.Println("Error:", err)
        }
        fmt.Println("GetStream:", stream)
        updateMysqlState(liveid, 2)  //stopped
        end := time.Now().Unix()
        name := "vod"             // required, string
        format := ""            // optional, string
        options:= pili.OptionalArguments{
            NotifyUrl: "",
            UserPipeline: "",
        } 
        
        var start int64
        mutex.Lock()
        if v, ok := chans[liveid]; ok {
            start =  v
        } else {
            start =  0
        }
        mutex.Unlock()

        saveAsRes, err := stream.SaveAs(name, format, int64(start), int64(end), options)
        if err != nil {
             fmt.Println("Error:", err)
        }
        fmt.Printf("SaveAs :%s\n", saveAsRes.Url)
        updateMysqlPlayback(liveid, saveAsRes.Url)
    }
}

func main(){
    chans = make(map[string]int64)
    http.HandleFunc("/newchannel", receive_new_live)
    http.HandleFunc("/stopchannel", stop_channel)
    err := http.ListenAndServe(":12345", nil)
    if err != nil {
    }
}
