### Простой REST-сервер

Сервер реализует простое *key-value* хранилище. Есть возможность записать json-сообщение по ключу, 
получить сообщение по ключу и удалить сообщение по ключу. Сообщения хранятся **postgres**.

### Балансировщик

Используется простой балансировщик, который перенаправляет все запросы на один из двух работающих серверов.
Успешные ответы на **GET** запросы кэшируются, и при повторном запросе возвращаются данные из кэша. При удалении, или повторной записи
по ключу данные из кэша удаляются. В качестве кэша используется **Redis**.

### Сервер поддреживает следующие запросы:

**GET** /messages/\<key:int> - получение значения с заданным ключом
 
  Ниже перечислены возможные ответы.
  
  * *Ключ найден*: 
    
    статус - 200, 
    сообщение - в теле ответа (в формате json)
  
  * *Ключ не найден*: 
  
    статус - 404

**DELETE** /messages/\<key:int> - удаление значения с заданным ключом
  
  Ниже перечислены возможные ответы.
  
  * *Ключ найден*:
   
    статус - 200
  
  * *Ключ не найден*:
   
    статус - 404

**POST** /messages/\<key:int> - создание сообщения для некоторого ключа. Тело запроса должно содержать валидный json.

  Ниже перечислены возможные ответы.
  
  * *Сообщение создано впервые*:
  
    статус - 201
    
  * *Сообщение перезаписано*:
    
    статус - 200 


### Что можно делать
1. Собрать образы командой `make build`
2. Запустить балансировщик (и все остальное) на порту **65432** командой `make start`.
3. Остановить все контейнеры командой `make stop`.
4. Удалить образы командой `make clean`.
