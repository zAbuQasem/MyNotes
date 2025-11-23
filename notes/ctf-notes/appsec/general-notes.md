# General Notes

## **Best approach so far to find Injections:**

1. See filtered special characters with the ffuf -> # To add a wordlist
2. Testing for basic injections with seclists wordlists (LFI, SQLI)
3. Testing cookies for injections especially when cookies contains regular data
4. Testing for SSTI (Java, Python...etc) not only on python apps
5. API could be vulnerable too!, So try with different request methods as a different method could handle a different functionality on the same endpoint!
6. How does the application handle other encodings? does it normalize it? (If YES then it's a possible attack vector)
7. Changing from captial to small or vice-verca is good to try
8. Don't forget the legacy XPATH Injection

## Testing JSON Data

1. Tampering the JSON structure could trigger an informative error
2. Some injections such as NOSQL ones require specific payloads
3. Always pay attention to special characters escaping especially quotes

## Authentication

1. Remove both username and password parameters and see the behavior (Some LDAP backends allow NULL sessions) or Weird PHP comparisions may lead to login bypass.

## Payment

1. Some applications errors if the cart/price is not an integer or a negative number, so try to add multiple items and try to subtract them from each other.

