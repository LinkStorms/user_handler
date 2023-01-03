import copy

import requests

from settings import DATA_LAYER


def get_data_layer_url():
    return f"{DATA_LAYER[1]}:{DATA_LAYER[2]}"


def check_reachability(service_name, service_url):
    try:
        response = requests.get(service_url)
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"Service {service_name} is not reachable.\nError: {e}")
    return True


def is_data_layer_reachable():
    data_layer_url = get_data_layer_url()
    return check_reachability("data_layer", data_layer_url)
