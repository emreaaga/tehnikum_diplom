from fastapi import Request, Body, UploadFile, APIRouter
from database.postservice import *
from urllib import request

posts_router = APIRouter(prefix="/posts", tags=["Post management"])


@posts_router.post("/api/add_post")
async def add_post(user_id: int, main_text: str, hashtag: str = None):
    new_post = public_post_db(user_id=user_id, main_text=main_text, hashtag=hashtag)
    if new_post:
        return {"status": 1, "message": "Post added successfully!"}
    return {"status": 0, "message": "Failed to add post!"}


@posts_router.get("/api/posts")
async def get_all_or_exact_post(post_id=0):
    post = get_all_or_exact_post_db(post_id)
    if post:
        return {"status": 1, "message": post}
    return {"status": 0, "message": "Post not found!"}


@posts_router.put("/api/posts")
async def change_user_post(post_id: int, new_text: str):
    if post_id and new_text:
        change_post_text(post_id=post_id, new_text=new_text)
        return {"status": 1, "message": "Post changed successfully!"}
    return {"status": 0, "message": "Error"}


@posts_router.delete("/api/posts")
async def delete_user_post(post_id: int):
    try:
        delete_post_db(post_id)
        return {"status": 1, "message": "Post deleted successfully!"}
    except:
        return {"status": 0, "message": "Delete post failed!"}
