from flask import Flask, request
from os import environ

from omegastar import handle_register

app = Flask(__name__)

@app.post("/register")
def register():
    api_key = environ.get("API_KEY")
    request_key = request.headers.get("x-api-key", "")

    if api_key != request_key:
        return "No", 403

    body = request.json
    username = body.get('username')
    token = body.get('token')
    email = body.get('email')

    if handle_register(username, email, token):
        return "Success", 200
    else:
        return "Failure", 418


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
