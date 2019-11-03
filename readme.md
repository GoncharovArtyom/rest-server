### Простой REST-сервер

Сервер реализует простое *key-value* хранилище. Есть возможность записать сообщение по ключу, 
получить сообщение по ключу и удалить сообщение по ключу. В качестве кэша используется **Redis**.
Все входящие запросы логируются в файле `/var/log/server.log`. 

##### Сервер поддреживает следующие запросы:

**GET** /messages/\<key:int> - получение значения с заданным ключом
 
  Ниже перечислены возможные ответы.
  
  * *Ключ найден*: 
    
    статус - 200, 
    сообщение в формате *JSON* - в теле ответа
  
  * *Ключ не найден*: 
  
    статус - 404

**DELETE** /messages/\<key:int> - удаление значения с заданным ключом
  
  Ниже перечислены возможные ответы.
  
  * *Ключ найден*:
   
    статус - 200
  
  * *Ключ не найден*:
   
    статус - 404

**POST** /messages/\<key:int> - создание сообщения для некоторого ключа. Сообщение должно быть передано в 
теле запроса в формате *JSON*.

  Ниже перечислены возможные ответы.
  
  * *Сообщение создано впервые*:
  
    статус - 201
    
  * *Сообщение перезаписано*:
    
    статус - 200 


##### Что можно делать
1. Собрать образы командой `make build`
2. Запустить сервер на порту **65432** командой `make start`.
3. Остановить сервер командой `make stop`.
4. Удалить образы командой `make clean`.