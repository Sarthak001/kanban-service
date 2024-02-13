from src import db
from src.models.verification_model import UserVerification


def create_verification(id,token_hash):
    verification = UserVerification(
                    user_id_fk=id,
                    token=token_hash,
                    consumed=False
    )
                
    db.session.add(verification)
    db.session.commit()
    return verification