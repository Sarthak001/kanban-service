from flask import render_template
from flask_mail import Message
from src import mail
from src import service

def send_mail(request, mail_details):
    with service.app_context():
        if request == "email verification":
            msg = Message("Almost there! Please verify your email address", sender="audit-noreply@gmail.com",
                        recipients=[mail_details["recipient"]])
            msg.html = render_template('mail_verification.html',
                                    data={"host": mail_details["host"], "token": mail_details["body-data"]})
            mail.send(msg)
        elif request == "user login verification":
            msg = Message("Sign In Otp Verification", sender="audit-noreply@gmail.com",
                        recipients=[mail_details["recipient"]])
            msg.html = render_template('mail_otp.html', data={"otp": mail_details["otp"],"user_info": mail_details["user_info"]})
            mail.send(msg)
        elif request == "password reset":
            pass
