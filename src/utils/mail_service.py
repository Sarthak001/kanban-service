from flask import render_template
from flask_mail import Message
from src import mail



def SendMail(requestType,mailDetails):
    if(requestType == "email verification"):
        msg = Message("Almost there! Please verify your email address", sender="audit-noreply@gmail.com",recipients=[mailDetails["recipient"]])
        msg.html = render_template('mail_verification.html',data={"host": mailDetails["host"] ,"token":mailDetails["bodydata"]})
        mail.send(msg)
    elif(requestType == "user login verification"):
        msg = Message("Login Otp Verification", sender="audit-noreply@gmail.com",recipients=[mailDetails["recipient"]])
        msg.html = render_template('mail_otp.html',data={"token":mailDetails["bodydata"]})
        mail.send(msg)