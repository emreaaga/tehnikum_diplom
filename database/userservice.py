from database.models import User
from database import get_db
from datetime import datetime
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('database.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def register_user_db(name, email, phone_number, password, user_city=None, birthday=None):
    db = next(get_db())
    checker = check_user_db(name, phone_number, email)
    if checker == True:
        new_user = User(name=name, email=email, phone_number=phone_number, password=password, user_city=user_city,
                        birthday=birthday, reg_date=datetime.now())
        db.add(new_user)
        db.commit()
        logger.info(f"Registered new user: {name}, {email}, {phone_number}")
        return new_user.id
    logger.warning(f"Registration failed for user: {name}, {email}, {phone_number}, Reason: {checker}")
    return checker


def check_user_db(name, phone_number, email):
    db = next(get_db())
    checker_name = db.query(User).filter_by(name=name).first()
    checker_phone = db.query(User).filter_by(phone_number=phone_number).first()
    checker_email = db.query(User).filter_by(email=email).first()
    if checker_name:
        return "This username already exist"
    elif checker_phone:
        return "This phone number already exist"
    elif checker_email:
        return "This email already exist"
    return True


def check_user_password_db(login, password):
    db = next(get_db())
    user_by_phone = db.query(User).filter_by(phone_number=login).first()
    user_by_email = db.query(User).filter_by(email=login).first()
    if user_by_phone:
        if user_by_phone.password == password:
            logger.info(f"User {user_by_phone.email} logged in successfully")
            return user_by_phone.id
    elif user_by_email:
        if user_by_email.password == password:
            logger.info(f"User {user_by_email.email} logged in successfully")
            return user_by_email.id
    logger.warning(f"Login attempt failed for login: {login}")
    return "Login error"


def profile_info_db(user_id):
    db = next(get_db())
    user_info = db.query(User).filter_by(id=user_id).first()
    if user_info:
        return user_info
    return False


def change_user_data_db(user_id, changeable_info, new_data):
    db = next(get_db())
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        try:
            if changeable_info == "name":
                user.name = new_data
                db.commit()
                return True
            elif changeable_info == "phone_number":
                user.phone_number = new_data
                db.commit()
                return True
            elif changeable_info == "email":
                user.email = new_data
                db.commit()
                return True
            elif changeable_info == "user_city":
                user.user_city = new_data
                db.commit()
                return True
            elif changeable_info == "password":
                user.password = new_data
                db.commit()
                return True
            elif changeable_info == "birthday":
                user.birthday = new_data
                db.commit()
                return True
        except Exception as e:
            return "Unfortunately at this moment change of data unavailable"
    return False
