from auth import OAuth
import requests


auth = OAuth()
headers = {'Authorization': f'bearer {auth.config["access_token"]}'}
r = requests.get(auth.url_root, headers=headers)
print(r.text)

