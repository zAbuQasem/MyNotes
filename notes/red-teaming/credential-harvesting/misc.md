# Miscellaneous
----
## Using image recognition
At times, when performing penetration tests, you might run across a large number of images. This could be images in S3 buckets or on a file share. It could also be images uploaded to a help-desk service ticket or JIRA—maybe screenshots from an application where customers can submit bugs. These images might contain Personal Identifiable Information (PII), and sometimes even passwords or access keys.
- Install [tesseract](https://github.com/tesseract-ocr/tesseract)
```bash
## On debian
sudo apt install tesseract-ocr
```
- Example:
```bash
tesseract <image>  <Output file>
## Ex: tesseract confedential.png result
## Text will be in result.txt
```
---
## Using transparent relay proxies for phishing
The idea is to stand up a malicious proxy on a phishing domain that just relays requests between the client and the destination. The destination would typically be a login page. When a victim gets phished and visits the malicious proxy, the experience for the user will be exactly the same as if the user had visited the actual login page. Remember that all requests are just relayed back and forth. However, the malicious proxy gains full access to passwords, multi-factor tokens, and so forth.

**There are a couple of tools out there to perform this kind of attack:**
- evilginx2: https://github.com/kgretzky/evilginx2
- Modlishka: https://github.com/drk1wi/Modlishka
- KoiPhish: https://github.com/wunderwuzzi23/KoiPhish

To mitigate these phishing attacks, **[FIDO2](https://fidoalliance.org/fido2/)** and **[WebAuthN](https://www.w3.org/TR/webauthn-1/)** have been developed. The basic idea is to leverage public key cryptography and dedicated authenticator devices (such as a security key) during the authentication flow. The browser is responsible for ensuring that only code running on the proper domain can access the corresponding keys on the device. This prevents the phishing proxy from accessing the keys.
> **Important Note:** 
> Environments might still be configured incorrectly, which can lead to successful phishing attacks. As an example, the MFA page, which interacts with the security device, is hosted on a different domain than the main login page where the user enters the password. In that case, an adversary might still be able to create a phishing page that mimics the entire flow and steal authentication tokens.