# arba_post_crud

A CRUD application for managing posts and comments

Live can be seen here if you wish to skip the hassle setup below: https://arba-post-crud.onrender.com/ <br>
Note: Let me know if the link is down & I will restart server, this is due server provider will slow down the server due to inactivity.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repository-name.git](https://github.com/syukranDev/arba_post_crud)
   cd arba_post_crude
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the local database (PostgreSQL) (optional as you can just use my live database):
   - Create a database, (optional: run migrations), and add initial data if needed. 
   ```
   CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL
   );
   
   CREATE TABLE posts (
       id SERIAL PRIMARY KEY,
       user_id VARCHAR(80) NOT NULL,
       title VARCHAR(255) NOT NULL,
       content TEXT NOT NULL,
       CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (username)
   );
   
   CREATE TABLE comments (
       id SERIAL PRIMARY KEY,
       post_id INTEGER NOT NULL,
       user_id VARCHAR(80) NOT NULL,
       content TEXT NOT NULL,
       CONSTRAINT fk_post FOREIGN KEY (post_id) REFERENCES posts (id),
       CONSTRAINT fk_comment_user FOREIGN KEY (user_id) REFERENCES users (username)
   );
   ```
   
   
## Usage

- Run the application:
  ```bash
  python app.py
  -- or run below, ensure you have Flask installed globally
  flask run --host=0.0.0.0 --port=9000
  ```
- Access the application at `http://localhost:9000`.

## Database Structure

The project uses a PostgreSQL database. The main tables are:
- **users**: Stores user credentials and metadata.
- **posts**: Contains posts created by users.
- **comments**: Stores comments on posts.
<img width="950" alt="image" src="https://github.com/user-attachments/assets/e5a2bbc1-6984-4e1d-9db4-d00a42512be0">


## Features

- User registration and authentication
- Protected API routes
- CRUD operations for posts and comments
- Dynamic relationships between users, posts, and comments

## Screenshots
<img width="820" alt="image" src="https://github.com/user-attachments/assets/30be1d49-e2db-4f66-85db-27d19f9060f2">

<img width="820" alt="image" src="https://github.com/user-attachments/assets/0befef22-e574-4455-a9df-5d9793a4a163">

<img width="799" alt="image" src="https://github.com/user-attachments/assets/d4de9e33-59f1-4473-832e-e1233af61f8c">


