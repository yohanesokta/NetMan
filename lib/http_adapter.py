import requests

class HttpAdapter:
    def fetch(self, url, method='GET', headers=None, body=None, body_type='json'):
        try:
            if body_type == 'json':
                response = requests.request(method, url, headers=headers, json=body)
            else: # form data
                response = requests.request(method, url, headers=headers, data=body)
            
            response.raise_for_status()  # Raise an exception for bad status codes
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return response.text
        except requests.exceptions.RequestException as e:
            return {"Errors": "Failed Request", "Errors Details": str(e)}
