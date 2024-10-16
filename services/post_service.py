from models.post_model import Post
from models.comment_model import Comment
from app import db

def create_post(user_id, title, content):
    post = Post(user_id=user_id, title=title, content=content)
    db.session.add(post)
    db.session.commit()
    return post

def update_post(post_id, user_id, title, content):
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()
    if post:
        post.title = title
        post.content = content
        db.session.commit()
    return post

def delete_post(post_id, user_id):
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return post

def create_comment(user_id, post_id, content):
    comment = Comment(user_id=user_id, post_id=post_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return comment

def update_comment(comment_id, user_id, content):
    comment = Comment.query.filter_by(id=comment_id, user_id=user_id).first()
    if comment:
        comment.content = content
        db.session.commit()
    return comment

def delete_comment(comment_id, user_id):
    comment = Comment.query.filter_by(id=comment_id, user_id=user_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return comment
