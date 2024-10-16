from app import db

def create_tables():
    db.create_all()
    print("All tables defined in models created successfully!")

if __name__ == '__main__':
    create_tables()
