import requests

class BubbleConnector:
    def __init__(self, app_name, api_token, version='live'):
        self.app_name = app_name
        self.api_token = api_token
        self.version = version
        self.base_url = f'https://{app_name}.bubbleapps.io/{version}/api/1.1/obj'
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

    def get_data(self, data_type, constraints=None):
        url = f'{self.base_url}/{data_type}'
        params = {'constraints': constraints} if constraints else {}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def create_data(self, data_type, data):
        url = f'{self.base_url}/{data_type}'
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_data(self, data_type, item_id, data):
        url = f'{self.base_url}/{data_type}/{item_id}'
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_data(self, data_type, item_id):
        url = f'{self.base_url}/{data_type}/{item_id}'
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def handle_mcp_template(self, template_data):
        # Example method to handle Bubble-generated MCP template
        return self.create_data('MCPTemplate', template_data)