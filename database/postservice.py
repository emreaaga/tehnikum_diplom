from database import get_db
from database.models import UserPost, Hashtag
from datetime import datetime


def get_all_or_exact_post_db(post_id):
    db = next(get_db())
    if post_id:
        exact_post = db.query(UserPost).filter_by(id=post_id).first()
        return exact_post
    elif post_id == 0:
        all_posts = db.query(UserPost).all()
        return [i for i in all_posts]


def change_post_text(post_id, new_text):
    db = next(get_db())
    post_to_edit = db.query(UserPost).filter_by(id=post_id).first()
    if post_to_edit:
        post_to_edit.main_text = new_text
        db.commit()
        return True
    return False


def delete_post_db(post_id):
    db = next(get_db())
    post_to_delete = db.query(UserPost).filter_by(id=post_id).first()
    if post_to_delete:
        db.delete(post_to_delete)
        db.commit()
        return True
    return False


def public_post_db(user_id, main_text, hashtag=None):
    db = next(get_db())
    new_post = UserPost(user_id=user_id, main_text=main_text, reg_date=datetime.now(), hashtag=hashtag)
    db.add(new_post)
    db.commit()
    return True


def add_hashtag(name):
    db = next(get_db())
    new_hashtag = Hashtag(hashtag_name=name, reg_date=datetime.now())
    db.add(new_hashtag)
    db.commit()
    return True


def get_exact_hashtag_db(hashtag_name):
    db = next(get_db())
    exact_hashtag = db.query(Hashtag).filter_by(hashtag_name=hashtag_name).first()
    return exact_hashtag
