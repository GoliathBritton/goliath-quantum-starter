import requests
import json

class DecentralizedClient:
    def __init__(self, api_url='https://chatapi.akash.network/api/v1'):
        self.api_url = api_url

    def deploy_compute_task(self, model, messages):
        """
        Deploy a compute task to Akash Network using the Chat API as an example of decentralized compute.
        """
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'model': model,
            'messages': messages
        }
        response = requests.post(f"{self.api_url}/chat/completions", headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error deploying task: {response.text}")