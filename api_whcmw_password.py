import requests
from pymongo import MongoClient


url = 'https://contabilitools.com.br/whmcs/includes/api.php'
data = {
    'action': 'GetClientPassword',
    'username': 'V3E02x1ZgILbSHoRmVcFyryTtqN4CUDw',
    'password': 'xX2A4DUhfuxU1PGk7p2xdS9SMM5j2wRM',
    'responsetype': 'json',
}

try:
    response = requests.post(url, data=data)
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
    else:
        print(f"Request Error: {response.status_code} - {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Request Exception: {e}")


