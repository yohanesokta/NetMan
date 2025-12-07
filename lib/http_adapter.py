import requests

class HttpAdapter:
    def __init__(self):
        self.request = requests

    def fetch(self, url, method='GET', headers=None, body=None, body_type='json'):
        try:
            if body_type == 'json':
                response = self.request.request(method, url, headers=headers, json=body)
            else:
                response = self.request.request(method, url, headers=headers, data=body)
            response.raise_for_status()
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return response.text

        except requests.exceptions.RequestException as e:
            return {"Errors": "Failed Request", "Errors Details": str(e)}
