from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'email.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'username@email.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/")
def index():
    msg = Message(subject='Hello World!', sender='noreply@MisterED.ca', recipients=['recipient@email.com'])
    msg.body = "Hello, World!"
    mail.send(msg)
    return "Message sent!"


if __name__ == '__main__':
    app.run(debug=True)
