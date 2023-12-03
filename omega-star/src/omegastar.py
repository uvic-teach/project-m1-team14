import requests
from random import randint
from os import environ
from datetime import timedelta
from redis import Redis
from rq import Queue
from notification import send_email

VALIDATE_URL = "https://fr1gi6xdtc.execute-api.us-west-2.amazonaws.com/prod/validate"


def handle_register(username: str, email: str, token: str, email_body: str) -> bool:
    if validate_request(username, token):
        next_availability = check_availability()
        schedule_notify(email, next_availability, email_body)
        return True
    else:
        return False


def validate_request(username: str, token: str) -> bool:
    api_key = environ.get("API_KEY")
    response = requests.get(VALIDATE_URL,
                            params={"username": username, "token": token},
                            headers={"X-Api-Key": api_key})
    return response.status_code == 200


def check_availability() -> int:
    return randint(30, 180)


def schedule_notify(email: str, notify_seconds: int, email_body: str):
    queue = Queue(connection=Redis(host="cache"))
    queue.enqueue_in(timedelta(seconds=notify_seconds),
                     func=notify, args=(email, email_body,))


def notify(email: str, email_body: str):
    print(f"emailing {email}")
    sender = environ.get("EMAIL_SENDER")

    if email_body == "": 
        send_email(sender,
                email,
                'Appointment notification',
                "It's time for your appointment!")
    else:
        send_email(sender,
                email,
                'Appointment notification',
                email_body)      
