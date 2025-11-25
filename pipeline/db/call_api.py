import requests
import json

def call_api(url: str, body: dict = None, method: str = "POST", headers: dict = None, timeout: int = 30):
    """
    Generic API caller with JSON body support.
    """

    default_headers = {
        "Content-Type": "application/json"
    }

    if headers:
        default_headers.update(headers)

    method = method.upper()
    method_map = {
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete
    }

    if method not in method_map:
        raise ValueError(f"Unsupported method: {method}")

    response = method_map[method](
        url,
        json=body,
        headers=default_headers,
        timeout=timeout
    )

    try:
        response.raise_for_status()
    except Exception as e:
        print("API Error:", e)
        print("Response:", response.text)
        raise

    try:
        return response.json()
    except:
        return response.text