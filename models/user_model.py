from app import db
from flask import jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    @staticmethod
    def verify_user(username, plain_password):
        try:
            user = User.query.filter_by(username=username).first()

            ##=====================================================
            ## bawah - debug output raw query result 
            attributes = vars(user)
            attributes.pop('_sa_instance_state', None)
            # print(attributes)  # show all user object value
            print(user.password_hash)
            ##=====================================================

            is_valid = bcrypt.checkpw(plain_password.encode('utf-8'), (user.password_hash).encode('utf-8')) 

            print(is_valid)
            if is_valid:
                return True
            return False
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            return False  
        except Exception as e:
            print(f"An error occurred: {e}")
            return False  

    @staticmethod
    def register_user(username, password):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(username=username, password_hash=hashed_password.decode('utf-8'))
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error occurred: {e}")
            return None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"An unexpected error occurred: {e}")
            return None