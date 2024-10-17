from flask import request, jsonify
from services.auth_service import decode_token
from services.post_service import (
    find_all_post, create_post, update_post, delete_post,
    find_all_comment, create_comment, update_comment, delete_comment
)

# ====================================================================
# DEVNOTE - Posts related endpoint goes below
# ====================================================================

def list_post_endpoint(decoded):
    user_id = decoded['username']

    posts = find_all_post(user_id) # we find all posts for logged in user only
    return jsonify(posts), 201

def create_post_endpoint(decoded):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = decoded['username']

    if not title:
        return jsonify({'errMsg': 'title is empty'}), 422
    if not content:
        return jsonify({'errMsg': 'content is empty'}), 422

    post = create_post(user_id, title, content)
    return jsonify(post.to_dict()), 201

def update_post_endpoint(post_id, decoded):
    data = request.get_json()
    print(data)
    title = data.get('title')
    content = data.get('content')
    user_id = decoded['username']

    if not title:
        return jsonify({'errMsg': 'title is empty'}), 422
    if not content:
        return jsonify({'errMsg': 'content is empty'}), 422

    post = update_post(post_id, user_id, title, content)
    return jsonify({'message': f'Successfully updated post ID - {post_id}'}), 201

def delete_post_endpoint(post_id, decoded):
    user_id = decoded['username']
    post = delete_post(post_id, user_id)
    return jsonify({'message': 'Post deleted'}), 201

# ====================================================================
# DEVNOTE - Comment related endpoint goes below
# ====================================================================
def list_comment_endpoint(post_id, decoded):
    posts = find_all_comment(post_id) # we find all commments related to that posts 
    return jsonify(posts), 201

def create_comment_endpoint(post_id, decoded):
    data = request.get_json()
    content = data.get('content')
    user_id = decoded['username']

    if not content:
        return jsonify({'errMsg': 'Content is empty'}), 422

    comment_response = create_comment(user_id, post_id, content)

    if isinstance(comment_response, tuple):
        return jsonify(comment_response[0]), comment_response[1]  

    return jsonify(comment_response.to_dict()), 201  

def update_comment_endpoint(comment_id, decoded):
    data = request.get_json()
    content = data.get('content')
    user_id = decoded['username']

    if not content:
        return jsonify({'errMsg': 'content is empty'}), 422

    comment = update_comment(comment_id, user_id, content)
    return jsonify({'message': 'Successfully updated comment'}), 201

def delete_comment_endpoint(comment_id, decoded):
    user_id = decoded['username']
    comment = delete_comment(comment_id, user_id)
    return jsonify({'message': 'Successfully deleted comment'}), 201