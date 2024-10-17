from models.post_model import Post
from models.comment_model import Comment
from app import db
from flask import jsonify

def find_all_post(user_id):
    # posts = Post.query.filter_by(user_id=user_id).all()
    posts = Post.query.all()
    return [post.to_dict() for post in posts]

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

def delete_post(post_id, user_id): # delete comments first then post
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()
    if post:
        comments = Comment.query.filter_by(post_id=post_id).all()
        for comment in comments:
                    db.session.delete(comment)

        db.session.delete(post)

        db.session.commit()
    return post

def find_all_comment(post_id):
    comments = Comment.query.filter_by(post_id=post_id)
    return [comment.to_dict() for comment in comments]

def create_comment(user_id, post_id, content):
    post = Post.query.get(post_id)
    if not post:
        # return jsonify({ 'errMsg' : "Post ID is not present in the posts table."}), 422
        return {"errMsg": "Post ID is not present in the posts table."}, 422

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
