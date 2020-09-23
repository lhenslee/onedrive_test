import json
import os
import requests


class OAuth:
    config = dict()
    client_id = str()
    tenant_id = str()
    scope = str()
    redirect_uri = str()
    client_secret = str()
    code = str()
    auth_base_url = str()
    token_url = str()
    url_root = str()

    def __init__(self):
        self.load_config()
        self.store_json_to_class_vars()
        if self.access_token_does_not_exist():
            self.get_token()
        self.get_token()

    def access_token_does_not_exist(self):
        if 'access_token' not in self.config.keys():
            return True
        return False

    def store_json_to_class_vars(self):
        self.client_id = self.config['clientId']
        self.tenant_id = self.config['tenantId']
        self.scope = self.config['scope']
        self.redirect_uri = self.config['redirectURI']
        self.url_root = self.config['url_root']
        self.auth_base_url = f'https://login.microsoftonline.us/{self.tenant_id}/oauth2/v2.0/authorize?'
        self.token_url = f'https://login.microsoftonline.us/{self.tenant_id}/oauth2/v2.0/token'

    def load_config(self):
        with open('settings.json', 'r') as f:
            self.config = json.load(f)

    def get_auth_request(self):
        auth_request = f'{self.auth_base_url}client_id={self.client_id}'\
                       f'&scope={self.scope}&response_type=code&redirect_uri={self.redirect_uri}'
        return auth_request

    '''
    POST https://login.microsoftonline.us/common/oauth2/v2.0/token
    Content-Type: application/x-www-form-urlencoded

    client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}
    &code={code}&grant_type=authorization_code    
    '''
    def get_code_post_response_in_json(self, code):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id, 'redirect_uri': self.redirect_uri,
            'client_secret': self.client_secret,
            'code': code, 'grant_type': 'authorization_code'
        }
        url = f'https://login.microsoftonline.us/{self.tenant_id}/oauth2/v2.0/token'
        raw_text = requests.post(url, data=data, headers=headers).text
        return json.loads(raw_text)

    '''
    POST https://login.microsoftonline.com/common/oauth2/v2.0/token
    Content-Type: application/x-www-form-urlencoded

    client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}
    &refresh_token={refresh_token}&grant_type=refresh_token
    '''
    def use_refresh_token(self, refresh_token):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id, 'redirect_uri': self.redirect_uri,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token, 'grant_type': 'refresh_token'
        }
        raw_text = requests.post(self.token_url, data=data, headers=headers).text
        return json.loads(raw_text)

    def get_token(self):
        auth_request = self.get_auth_request()
        os.system(f'start "" "{auth_request}"')
        response_uri = input('Please input the redirect URL:\n')
        code = response_uri.split('code=')[1].split('&')[0]
        code_response = self.get_code_post_response_in_json(code)
        self.config['code'] = code
        self.config['access_token'] = code_response['access_token']
        self.config['refresh_token'] = code_response['refresh_token']
        self.config['id_token'] = code_response['id_token']
        with open('settings.json', 'w') as f:
            json.dump(self.config, f, indent=2)

