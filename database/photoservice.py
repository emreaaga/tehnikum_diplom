from database import get_db
from database.models import PostPhoto
from datetime import datetime


def add_photo_db(post_id, photo_path):
    db = next(get_db())
    photo = PostPhoto(post_id=post_id, photo_path=photo_path, reg_date=datetime.now())
    db.add(photo)
    db.commit()
    return post_id


