import requests
from bardapi import SESSION_HEADERS
from bardapi import Bard

token = "ewgWvipOanGFgIkAby_kqlj1GCrE13fStypAvRcaFhdgYhuamk5Nlvllv5ikLY6tnASTnA."
session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID", token)
session.cookies.set("__Secure-1PSIDTS","xxxxx")
session.cookies.set("__Secure-1PSIDCC","xxxxx")

bard = Bard(token=token, session=session)

print(bard.get_answer("Hi")['content'])
