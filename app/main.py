from secrets import token_hex

from flask import Flask, json, request
from werkzeug.exceptions import HTTPException
import requests

from settings import HOST, PORT, ACCESS_TOKEN_BYTE_SIZE
from communications import login, register
from utilities import (
    store_token,
    return_token_if_exists,
    delete_token,
    check_token,
)

app = Flask(__name__)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        # "name": e.name,
        "data": {},
        "errors": [e.description],
    })
    response.content_type = "application/json"
    return response


@app.route("/access_token", methods=["POST"])
def access_token_endpoint():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    response = login(username, password)

    status_code = response["code"]

    if status_code == 200:
        user_id = response["data"]["user_id"]
        existing_token = return_token_if_exists(user_id)
        if existing_token:
            response["data"] = {
                "user_id": user_id,
                "access_token": existing_token
            }
            return response, status_code
        access_token = token_hex(ACCESS_TOKEN_BYTE_SIZE)
        store_token(user_id, access_token)
        response["data"] = {
            "user_id": user_id,
            "access_token": access_token
        }
        return response, status_code

    if status_code == 400 or status_code == 404:
        response["code"] = 401
        response["errors"] = ["Invalid username or password"]
        return response, status_code
    
    return response, status_code


@app.route("/delete_token", methods=["POST"])
def delete_token_endpoint():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    response = login(username, password)

    status_code = response["code"]

    if status_code == 200:
        user_id = response["data"]["user_id"]
        delete_token(user_id)
        response["data"] = {
            "user_id": user_id,
        }
        return response, status_code

    if status_code == 400 or status_code == 404:
        response["code"] = 401
        response["errors"] = ["Invalid username or password"]
        return response, status_code
    
    return response, status_code


@app.route("/check_token", methods=["POST"])
def check_token_endpoint():
    access_token = request.json.get("access_token", "")
    try:
        user_id = check_token(access_token)
    except Exception as e:
        return {
            "code": 401,
            "data": {},
            "errors": [str(e)],
        }, 401
    return {
        "code": 200,
        "data": {
            "user_id": user_id,
        },
        "errors": [],
    }, 200


@app.route("/register", methods=["POST"])
def register_endpoint():
    username = request.json.get("username", "")
    password = request.json.get("password", "")
    email = request.json.get("email", "")

    response = register(username, password, email)

    return response, response["code"]


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
