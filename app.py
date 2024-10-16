# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()  # Instantiate SQLAlchemy without the app instance
migrate = Migrate()  # Instantiate Migrate without the app instance

def create_app():
    app = Flask(__name__)

    # Set configurations
    app.config['SECRETKEY_JWT'] = os.getenv('SECRETKEY_JWT')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional

    # Initialize the database and migration
    db.init_app(app)  # Bind the app to the db instance
    migrate.init_app(app, db)  # Bind the app to the migrate instance

    # Function to check database connection
    def check_db_connection():
        try:
            # Attempt to connect to the database by executing a simple query
            db.session.execute(text('SELECT 1'))   # This is a lightweight query
            print("Database connection successful.")
        except Exception as e:
            print(f"Database connection failed: {e}")

    # Check DB connection when the app is created
    with app.app_context():
        check_db_connection()

    # Import models to avoid circular imports later
    from models.user_model import User
    from models.post_model import Post
    from models.comment_model import Comment
  

    # Import controllers after models
    from controllers import auth_controller, post_controller

    # Define routes
    @app.route('/test', methods=['POST'])
    def test_route():
        return {'message': 'Hello, this is a test route'}

    app.route('/login', methods=['POST'])(auth_controller.login)

    app.route('/register', methods=['POST'])(auth_controller.register)

    @app.route('/protected', methods=['GET'])
    def protected():
        return auth_controller.protected()

    # Post Routes
    @app.route('/posts', methods=['POST'])
    def create_post():
        return post_controller.create_post_endpoint()

    @app.route('/posts/<int:post_id>', methods=['PUT'])
    def update_post(post_id):
        return post_controller.update_post_endpoint(post_id)

    @app.route('/posts/<int:post_id>', methods=['DELETE'])
    def delete_post(post_id):
        return post_controller.delete_post_endpoint(post_id)

    # Comment Routes
    @app.route('/posts/<int:post_id>/comments', methods=['POST'])
    def create_comment(post_id):
        return post_controller.create_comment_endpoint(post_id)

    @app.route('/comments/<int:comment_id>', methods=['PUT'])
    def update_comment(comment_id):
        return post_controller.update_comment_endpoint(comment_id)

    @app.route('/comments/<int:comment_id>', methods=['DELETE'])
    def delete_comment(comment_id):
        return post_controller.delete_comment_endpoint(comment_id)

    return app 

if __name__ == '__main__':
    app = create_app()  
    app.run(debug=True)
