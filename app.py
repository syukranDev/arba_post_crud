# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from middleware.auth_middleware import token_required

load_dotenv();

db = SQLAlchemy() 
migrate = Migrate()  

def create_app():
    app = Flask(__name__)

    app.config['SECRETKEY_JWT'] = os.getenv('SECRETKEY_JWT')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional

    db.init_app(app) 
    migrate.init_app(app, db) 

    def check_db_connection(): #test connection
        try:
            db.session.execute(text('SELECT 1'))   
            print("Database connection successful.")
        except Exception as e:
            print(f"Database connection failed: {e}")

    with app.app_context():
        check_db_connection()

    #  DEVNOTE: Import models then controller globally to avoid circular imports
    from models.user_model import User
    from models.post_model import Post
    from models.comment_model import Comment
    from controllers import auth_controller, post_controller

    @app.route('/test', methods=['POST'])
    def test_route():
        return {'message': 'Hello, this is a test route'}

    app.route('/login', methods=['POST'])(auth_controller.login)
    app.route('/register', methods=['POST'])(auth_controller.register)

    # @app.route('/protected', methods=['GET']) 
    # def protected():
    #     return auth_controller.protected()

    # Post Routes
    @app.route('/posts/create', methods=['POST'])
    @token_required
    def create_post(decoded_token):
        return post_controller.create_post_endpoint(decoded_token)

    @app.route('/posts/update/<int:post_id>', methods=['POST'])
    @token_required
    def update_post(post_id, decoded_token):
        return post_controller.update_post_endpoint(post_id, decoded_token)

    @app.route('/posts/delete/<int:post_id>', methods=['POST'])
    @token_required
    def delete_post(post_id, decoded_token):
        return post_controller.delete_post_endpoint(post_id, decoded_token)

    # Comment Routes
    @app.route('/posts/<int:post_id>/comments/create', methods=['POST'])
    @token_required
    def create_comment(post_id, decoded_token): # we need post id so the comment creted will associated to the post id
        return post_controller.create_comment_endpoint(post_id, decoded_token)

    @app.route('/comments/<int:comment_id>/update', methods=['POST'])
    @token_required
    def update_comment(comment_id, decoded_token):
        return post_controller.update_comment_endpoint(comment_id, decoded_token)

    @app.route('/comments/<int:comment_id>/delete', methods=['POST'])
    @token_required
    def delete_comment(comment_id, decoded_token):
        return post_controller.delete_comment_endpoint(comment_id, decoded_token)

    return app 

if __name__ == '__main__':
    app = create_app()  
    app.run(debug=True)
