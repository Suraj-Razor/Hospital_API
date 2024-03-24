from models.user import User
import functools
from flask_jwt_extended import get_jwt_identity
from init import db 

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {"error":f"Not authorised to perform action - {fn.__name__}"}, 403
    return wrapper