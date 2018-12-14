import json
import requests
from GenJWT import JwtManager

def lambda_handler(event, context):
    installation_id = event['installation']['id']
    manager = JwtManager()

    BASE_URL = event["pull_request"]["issue_url"] + "/comments"
    TO_USER = event["pull_request"]["user"]["login"]
    # TODO implement
    text = "@{} LGTM! いい感じだよ!".format(TO_USER)
    body = {
        "body": text
    }
    if event['action'] == "opened" or event['action'] == "closed":
        r = requests.post(BASE_URL, json=body, headers = manager.getToken(installation_id))
        #r = requests.post(BASE_URL, json=body)
        if not r.ok:
            return {
                'statusCode': 500,
                'body': json.dumps('Do not work well')
            }
        else:
            return {
                    'statusCode': 200,
                    'body': json.dumps('It works')
                }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('NOT SUPPORTED NOW')
        }
