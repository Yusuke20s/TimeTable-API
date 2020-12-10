# TimeTable Web API  

## 概要  

時間割データをjsonで返すWeb API  

## 時間割データ  

Google Sheets を使用  
時間割変更にも対応（人力でSheetsに記載必須）  

### 記載形式  

シート名: 曜日名（英語）  
Ex）Monday  

||A|B|C|D|E|F|
|-|-|-|-|-|-|-|
|1||1組|2組|3組|4組|5組|
|2|1st||||||
|3|2nd||||||
|4|3rd||||||
|5|4th||||||
|6|5th||||||
|7|6th||||||
|8|7th||||||
|9|8th||||||

### 時間割変更記載形式  

シート名: mm/dd（0も含める）  
Ex）01/01  

||A|B|C|D|E|F|
|-|-|-|-|-|-|-|
|1||1組|2組|3組|4組|5組|
|2|1st|None|None|None|None|None|
|3|2nd|None|None|None|None|None|
|4|3rd|None|None|None|None|None|
|5|4th|None|None|None|None|None|
|6|5th|None|None|None|None|None|
|7|6th|None|None|None|None|None|
|8|7th|None|None|None|None|None|
|9|8th|None|None|None|None|None|

変更箇所のみ、その旨記載  

## Json形式  

{  
    "1":[1限, 2限, 3限, 4限, 5限, 6限, 7限, 8限],  
    "2":[1限, 2限, 3限, 4限, 5限, 6限, 7限, 8限],  
    "3":[1限, 2限, 3限, 4限, 5限, 6限, 7限, 8限],  
    "4":[1限, 2限, 3限, 4限, 5限, 6限, 7限, 8限],  
    "5":[1限, 2限, 3限, 4限, 5限, 6限, 7限, 8限],  
}  

時間割変更がある授業は授業名の前に☆がつく  