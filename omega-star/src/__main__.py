from flask import Flask, request, make_response

from omegastar import handle_register

app = Flask(__name__)


@app.route("/register", methods=['OPTIONS', 'POST'])
def register():
    if request.method == 'OPTIONS':
        return build_preflight()
    elif request.method == 'POST':
        return build_response(request)


def build_response(request):
    body = request.json
    username = body.get('username')
    token = body.get('token')
    email = body.get('email')
    email_body = body.get('email_body')

    if handle_register(username, email, token, email_body):
        response = make_response("Success", 200)
    else:
        response = make_response("Failure", 401)

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def build_preflight():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
