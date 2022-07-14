# Navigation
- [**AWS-KMS**](#AWS-KMS)
	- [KMS-CMK](#KMS-CMK)
	- [KMS-Automatic-Key-Rotation](#KMS-Automatic-Key-Rotation)
	- [KMS-Manual-Key-Rotation](#KMS-Manual-Key-Rotation)
	- [[#]]
# AWS-KMS
- **KMS**: Key Management Service
- Easy way to control access to your data, AWS manages keys for us  
- Fully integrated with IAM for authorization
- Three types of Customer Master Keys (CMK):  
	- AWS Managed Service Default CMK: free  
	- User Keys created in KMS: $1 / month  
	- User Keys imported (must be 256-bit symmetric key): $1 / month
- **KMS can only help in encrypting up to 4KB of data per call**  
- **If data > 4 KB, use envelope encryption**
## KMS-CMK
**CMK**: Custom Master Key
- **Symmetric (AES-256)**
	- First offering of KMS, single encryption key that is used to Encrypt and Decrypt  
	- AWS services that are integrated with KMS use Symmetric CMKs
	- Necessary for envelope encryption  
	- You never get access to the Key unencrypted (must call KMS API to use)
- **Asymmetric (RSA & ECC key pairs)**  
	- Public (Encrypt) and Private Key (Decrypt) pair  
	- Used for Encrypt/Decrypt, or Sign/Verify operations  
	- The public key is downloadable, but you can’t access the Private Key unencrypted  
	- **Use case**: encryption outside of AWS by users who can’t call the KMS API
## KMS-Automatic-Key-Rotation
- **For Customer-managed CMK** (not AWS managed CMK)  
- If enabled: automatic key rotation happens every 1 year  
- Previous key is kept active so you can decrypt old data  
- New Key has the same CMK ID (only the backing key is changed)
## KMS-Manual-Key-Rotation
- **When you want to rotate key every 90 days, 180 days, etc...**  
- New Key has a different CMK ID  
- Keep the previous key active so you can decrypt old data  
- Better to use aliases in this case (to hide the change of key for the application)  
- Good solution to rotate CMK that are not eligible for automatic rotation (like asymmetric CMK)
