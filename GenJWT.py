import os
from os.path import join, dirname
from datetime import datetime, timedelta
import requests
import json
import jwt
from dotenv import load_dotenv
from Crypto.PublicKey import RSA

# Refered: https://github.com/chakki-works/typot/blob/master/typot/env.py
class JwtManager():
    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

    # Get PRIVATE KEY Of GitHub
    def get_private_pem(self):
        key = os.environ.get("PRIVATE_KEY","")
        return key

    def get_app_id(self):
        return os.environ.get("APP_ID", 0)

    # Get token of GitHub
    def getToken(self, installation_id):
        utcnow = datetime.utcnow() + timedelta(seconds=-5)
        duration = timedelta(seconds=30)
        payload = {
            "iat": utcnow,
            "exp": utcnow + duration,
            "iss": self.get_app_id()
        }
        pem = self.get_private_pem()
        rsa_key = RSA.importKey(pem)
        key = rsa_key.exportKey()
        encoded = jwt.encode(payload, key, "RS256")
        headers = {
            "Authorization": "Bearer " + encoded.decode("utf-8"),
            "Accept": "application/vnd.github.machine-man-preview+json"
        }
        auth_url = "https://api.github.com/installations/{}/access_tokens".format(installation_id)
        r = requests.post(auth_url, headers=headers)

        if not r.ok:
            print(r.json()["message"])
            r.raise_for_status()
        token = r.json()["token"]
        return {
            "Authorization": "token {}".format(token)
        }

if __name__ == "__main__":
    manager = JwtManager()
