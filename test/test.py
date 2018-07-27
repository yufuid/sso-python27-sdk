import os
import YufuAuth

path = os.path.abspath('.')
private_key = open("test/private.pem", "r").read()
public_key = open("test/public.pem", "r").read()

idp = YufuAuth.YufuAuth.Builder().role("IDP").issuer("test-iss").privateKeyPath("test/private.pem").build()
token = idp.generateToken({'some': 'payload'})

serviceProvider = YufuAuth.YufuAuth.Builder().role("SP").publicKeyPath('test/public.pem').build()
claims = serviceProvider.verify(token)