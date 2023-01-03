import copy
import dbm

import requests

from settings import DATA_LAYER, DB_PATH


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


def store_token(user_id, access_token, db_path=DB_PATH):
    with dbm.open(db_path, "c") as db:
        db[access_token] = str(user_id)
