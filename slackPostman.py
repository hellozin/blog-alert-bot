import requests
import json

def send(message):
    webhook_url = 'https://hooks.slack.com/services/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'
    payload = {'text': message}

    requests.post(
        webhook_url, data = json.dumps(payload),
        headers = {'Content-Type': 'application/json'}
        )
