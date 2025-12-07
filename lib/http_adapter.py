import requests

class HttpAdapter:
    def fetch(self, url, method='GET', headers=None, body=None):
        try:
            response = requests.request(method, url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for bad status codes
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                return response.text
        except requests.exceptions.RequestException as e:
            return {"Errors": "Failed Request", "Errors Details": str(e)}
