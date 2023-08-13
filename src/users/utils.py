import os
from dotenv import load_dotenv
from emails import Message

load_dotenv()


def send_registration_email(email, username):
    message = Message(
        subject="Registration Confirmation",
        mail_from=("Your Name", "Суперпупур имейл"),
        text="Thank you for registering with us!",
        html=f"<p>Thank you for registering with us!</p><p>Your registration details:</p><p>Email: {email}</p><p>Username: {username}</p>",
    )

    message.send(to=email, smtp={"host": "smtp.gmail.com", "port": 587, "tls": True,
                                 "user": os.getenv('SMTP_USER'),
                                 "password": os.getenv('SMTP_PASSWORD')})


