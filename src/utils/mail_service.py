from flask import render_template
from flask_mail import Message
from src import mail


def send_mail(request, mail_details):
    if request == "email verification":
        msg = Message("Almost there! Please verify your email address", sender="audit-noreply@gmail.com",
                      recipients=[mail_details["recipient"]])
        msg.html = render_template('mail_verification.html',
                                   data={"host": mail_details["host"], "token": mail_details["body-data"]})
        mail.send(msg)
    elif request == "user login verification":
        msg = Message("Sign In Otp Verification", sender="audit-noreply@gmail.com",
                      recipients=[mail_details["recipient"]])
        msg.html = render_template('mail_otp.html', data={"otp": mail_details["otp"]})
        mail.send(msg)
    elif request == "password reset":
        pass
