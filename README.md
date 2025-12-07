# ⚡ ~~POST~~ NET Man
|   *blazingly fast* **API CLIENT**

## HTTP Adapter

This project uses an `HttpAdapter` class to standardize making HTTP requests. The adapter provides a `fetch` method that simplifies interacting with APIs by providing a consistent interface for various HTTP methods.

### `HttpAdapter.fetch(url, method='GET', headers=None, body=None)`

-   **`url`**: The URL for the request.
-   **`method`**: The HTTP method to use (e.g., 'GET', 'POST', 'PUT', 'DELETE'). Defaults to 'GET'.
-   **`headers`**: A dictionary of headers to include with the request.
-   **`body`**: A dictionary representing the JSON payload for the request.

The `fetch` method returns a dictionary, which is the JSON response from the server. If the request fails, it returns a dictionary with an "Errors" key containing details about the failure.

### Example Usage

```python
from lib.http_adapter import HttpAdapter

adapter = HttpAdapter()

# Example GET request
response = adapter.fetch('https://api.example.com/data')
print(response)

# Example POST request with headers and body
headers = {'Authorization': 'Bearer YOUR_TOKEN'}
body = {'key': 'value'}
response = adapter.fetch('https://api.example.com/data', method='POST', headers=headers, body=body)
print(response)
```
