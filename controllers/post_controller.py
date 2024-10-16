from flask import request, jsonify
from services.auth_service import decode_token
from services.post_service import (
    create_post, update_post, delete_post,
    create_comment, update_comment, delete_comment
)

def create_post_endpoint():
    token = request.headers.get('Authorization')
    decoded = decode_token(token)
    if decoded in ["expired", "invalid"]:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = decoded['username']

    post = create_post(user_id, title, content)
    return jsonify(post.to_dict()), 201

def update_post_endpoint(post_id):
    token = request.headers.get('Authorization')
    decoded = decode_token(token)
    if decoded in ["expired", "invalid"]:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = decoded['username']

    post = update_post(post_id, user_id, title, content)
    return jsonify(post.to_dict()) if post else jsonify({'message': 'Post not found or unauthorized'}), 404

def delete_post_endpoint(post_id):
    token = request.headers.get('Authorization')
    decoded = decode_token(token)
    if decoded in ["expired", "invalid"]:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = decoded['username']
    post = delete_post(post_id, user_id)
    return jsonify({'message': 'Post deleted'}) if post else jsonify({'message': 'Post not found or unauthorized'}), 404

def create_comment_endpoint(post_id):
    token = request.headers.get('Authorization')
    decoded = decode_token(token)
    if decoded in ["expired", "invalid"]:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    content = data.get('content')
    user_id = decoded['username']

    comment = create_comment(user_id, post_id, content)
    return jsonify(comment.to_dict()), 201

def update_comment_endpoint(comment_id):
    token = request.headers.get('Authorization')
    decoded = decode_token(token)
    if decoded in ["expired", "invalid"]:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    content = data.get('content')
    user_id = decoded['username']

    comment = update_comment(comment_id, user_id, content)
    return jsonify(comment.to_dict()) if comment else jsonify({'message': 'Comment not found or unauthorized'}), 404

def delete_comment_endpoint(comment_id):
    token = request.headers.get('Authorization')
    decoded = decode_token(token)
    if decoded in ["expired", "invalid"]:
        return jsonify({'message': 'Unauthorized'}), 401

    user_id = decoded['username']
    comment = delete_comment(comment_id, user_id)
    return jsonify({'message': 'Comment deleted'}) if comment else jsonify({'message': 'Comment not found or unauthorized'}), 404
