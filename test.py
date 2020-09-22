import json
import requests


class OAuth:
    config = dict()
    client_id = str()
    tenant_id = str()
    scope = str()
    redirect_uri = str()
    client_secret = str()
    code = str()

    def __init__(self):
        self.load_config()
        self.store_json_to_class_vars()

    def store_json_to_class_vars(self):
        self.client_id = self.config['clientId']
        self.tenant_id = self.config['tenantId']
        self.scope = self.config['scope']
        self.redirect_uri = self.config['redirectURI']
        self.client_secret = self.config['clientSecret']
        self.code = self.config['code']

    def load_config(self):
        with open('settings.json', 'r') as f:
            self.config = json.load(f)

    def get_auth_request(self):
        auth_request = f'https://login.microsoftonline.us/{self.tenant_id}/oauth2/v2.0/authorize?'\
                       f'client_id={self.client_id}'\
                       f'&scope={self.scope}&response_type=code&redirect_uri={self.redirect_uri}'
        return auth_request

    '''
    POST https://login.microsoftonline.us/common/oauth2/v2.0/token
    Content-Type: application/x-www-form-urlencoded

    client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}
    &code={code}&grant_type=authorization_code    
    '''
    def post_code(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id, 'redirect_uri': self.redirect_uri,
            #'client_secret': self.client_secret,
            'code': self.code, 'grant_type': 'authorization_code'
        }
        url = f'https://login.microsoftonline.us/{self.tenant_id}/oauth2/v2.0/token'
        return requests.post(url, data=data, headers=headers)


auth = OAuth()
print(auth.get_auth_request())
print(auth.post_code().text)

