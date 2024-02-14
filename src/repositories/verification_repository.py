from src import db
from src.models.verification_model import UserVerification
from src.models.user_model import User
from src.models.otp_model import Otp
from src.models.password_reset_model import PasswordReset
from src.utils import otp_service
import hashlib


def create_verification(id,token_hash):
    verification = UserVerification(
        user_id_fk=id,
        token=token_hash,
        consumed=False
    )
                
    db.session.add(verification)
    db.session.commit()
    return verification


def get_verification(email,token):
    db_res = db.session.query(User.email, UserVerification.token, UserVerification.expire_in).join(
            User.verification).filter(User.email == email, UserVerification.token == token).order_by(
            UserVerification.id.desc()).first()
    return db_res


def create_otp(user):
    one_time_code = str(otp_service.GenerateOtp())
    otp_obj = Otp(
        user_id_fk=user.user_id,         
        otp=one_time_code
    )     
    db.session.add(otp_obj)
    db.session.commit()
    return one_time_code


def get_otp(email,otp):
    db_res = db.session.query(User.email, Otp.otp, Otp.expire_in) \
            .join(User.otp).filter(User.email == email, Otp.otp == otp) \
            .order_by(Otp.id.desc()).first()
    return db_res

def create_password(user):
    passwd_obj = PasswordReset(
                user_id_fk=user.user_id,
                token=hashlib.md5(f"{user['email']}".encode('utf-8')).hexdigest(),
                consumed=False
            )
    db.session.add(passwd_obj)
    db.session.commit()
    

def get_password_reset(email,token):
    db_res = db.session.query(User.is_active, PasswordReset.expire_in, PasswordReset.consumed).join(
                User.reset_pd).filter(
                User.email == email, PasswordReset.token == token).order_by(PasswordReset.id.desc()).first()
    return db_res