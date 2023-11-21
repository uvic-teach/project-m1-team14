from flask import Flask, request, make_response

from omegastar import handle_register

app = Flask(__name__)


@app.post("/register")
def register():
    body = request.json
    username = body.get('username')
    token = body.get('token')
    email = body.get('email')

    if handle_register(username, email, token):
        response = make_response("Success", 200)
    else:
        response = make_response("Failure", 403)

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
