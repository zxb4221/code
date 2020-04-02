package main

import "fmt"
import "net/http"
import "io/ioutil"
import "os"
import "encoding/json"
import "strings"
import "strconv"

type PricePair struct{
    CurrencyA string
    CurrencyB string
    ExchangeValue float64
}

func main(){
    
    A_B := PricePair{"a","b",0.00000028}
    C_A := PricePair{"b","c",1/0.00001819}
    B_C := PricePair{"c","a",1/0.01576}
    arrPricePair := [3]PricePair{}
    arrPricePair[0] = A_B
    arrPricePair[1] = B_C
    arrPricePair[2] = C_A
    
    
    //getPoloniexData()
    data, _ := ReadData("./data.json")
    
    var obj map[string]interface{}
    if err := json.Unmarshal(data, &obj); err != nil {
        fmt.Println(err)
    } 
    
    var nameMap map[string]bool
    nameMap = make(map[string]bool)

    
    var priceMap map[string]float64
    priceMap = make(map[string]float64)

    for k, v := range obj {
        price := (v.(map[string]interface{}))["last"]
        arr_name := strings.Split(k, "_")
        value, err := strconv.ParseFloat(price.(string), 64)
        if err != nil{
            fmt.Println(err)
        }
        nameMap[arr_name[0]] = true
        nameMap[arr_name[1]] = true
        priceMap[arr_name[1] + "_" + arr_name[0]] = value
        priceMap[arr_name[0] + "_" + arr_name[1]] = 1/value
    }
    /*
    for k, v := range priceMap{
        fmt.Printf("%s:%.12f\n", k, v)
    }
    */
    count := 0
    for k1,_ := range nameMap{
        for k2,_ := range nameMap{
            for k3,_ := range nameMap{
                if k1 != k2 && k2 != k3{
                    v1, ok1 := priceMap[k1 + "_" + k2]
                    v2, ok2 := priceMap[k2 + "_" + k3]
                    v3, ok3 := priceMap[k3 + "_" + k1]
                    if(ok1 && ok2 && ok3){
                        //fmt.Printf("%s:%.12f\n", k1 + "_" + k2, v1)
                        //fmt.Printf("%s:%.12f\n", k2 + "_" + k3, v2)
                        //fmt.Printf("%s:%.12f\n", k3 + "_" + k1, v3)
                        
                        result := v1*v2*v3
                        if result > 1.01{
                            count += 1
                            fmt.Printf("%1.4f,%s->%s(%.10f)->%s(%.10f)->%s(%.10f)\n", result, k1, k2, v1, k3, v2, k1, v3)
                        }
                    }
                }
            }
        }
    }
    fmt.Printf("count:%d\n", count)
    
}

func ReadData(filePth string) ([]byte, error) {
 f, err := os.Open(filePth)
 if err != nil {
  return nil, err
 }
 

 return ioutil.ReadAll(f)
}

func getResult(arr [3]PricePair)(float64){
    var result float64 = 0.0
    
    arr_size := len(arr)
    result = arr[0].ExchangeValue
    for i:= 0; i < arr_size; i++{
        fmt.Printf("%s->%s:%.12f\n",arr[i].CurrencyA, arr[i].CurrencyB, arr[i].ExchangeValue)
        if i < len(arr)-1{
            result = result*arr[i+1].ExchangeValue
        }
    }
    return result
}

func getPoloniexData(){
    address := "http://poloniex.com/public?command=returnTicker"
    client := &http.Client{}
    reqest, _ := http.NewRequest("GET", address, nil)
    
   
    response,_ := client.Do(reqest)
    if response.StatusCode == 200 {
        body, _ := ioutil.ReadAll(response.Body)
        bodystr := string(body);
        fmt.Println(bodystr)
    }else{
        fmt.Println(response.StatusCode)
    }    

    defer response.Body.Close()
 
 
}







