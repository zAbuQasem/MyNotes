# 0Auth

## Recon

Once you know the hostname of the authorization server, you should always try sending a `GET` request to the following standard endpoints:

* `/.well-known/oauth-authorization-server`
* `/.well-known/openid-configuration`

These will often return a JSON configuration file containing key information, such as details of additional features that may be supported. This will sometimes tip you off about a wider attack surface and supported features that may not be mentioned in the documentation.

