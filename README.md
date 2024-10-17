# arba_post_crud

A CRUD application for managing posts and comments

Live can be seen here if you wish to skip the hassle setup below: https://arba-post-crud.onrender.com/


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
   - Create a database, run migrations, and add initial data if needed. 
   
## Usage

- Run the application:
  ```bash
  python app.py
  -- or run below
  flask --app app.py --debug run
  ```
- Access the application at `http://localhost:5000`.

## Database Structure

The project uses a PostgreSQL database. The main tables are:
- **users**: Stores user credentials and metadata.
- **posts**: Contains posts created by users.
- **comments**: Stores comments on posts.
<img width="950" alt="image" src="https://github.com/user-attachments/assets/e5a2bbc1-6984-4e1d-9db4-d00a42512be0">


## Features

- User registration and authentication
- CRUD operations for posts and comments
- Dynamic relationships between users, posts, and comments

## Screenshots
<img width="820" alt="image" src="https://github.com/user-attachments/assets/30be1d49-e2db-4f66-85db-27d19f9060f2">

<img width="820" alt="image" src="https://github.com/user-attachments/assets/0befef22-e574-4455-a9df-5d9793a4a163">

<img width="799" alt="image" src="https://github.com/user-attachments/assets/d4de9e33-59f1-4473-832e-e1233af61f8c">


