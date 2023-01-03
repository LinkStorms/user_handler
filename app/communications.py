import requests

from utilities import get_data_layer_url


def login(username, password, data_layer_url=get_data_layer_url()):
    url = f"{data_layer_url}/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response.json()


def register(username, password, email, data_layer_url=get_data_layer_url()):
    url = f"{data_layer_url}/create_user"
    payload = {"username": username, "password": password, "email": email}
    response = requests.post(url, json=payload)
    return response.json()


def add_service_token(user_id, token, token_name, data_layer_url=get_data_layer_url()):
    url = f"{data_layer_url}/create_token"
    payload = {"user_id": user_id, "token": token, "token_name": token_name}
    response = requests.post(url, json=payload)
    return response.json()
