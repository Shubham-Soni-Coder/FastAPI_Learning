# from database import engine, get_db
# from models import Base, User
# from database import session

# from sqlalchemy import inspect


# # This line actually CREATES the database and tables
# Base.metadata.create_all(bind=engine)

# db = session()


# def user_crete(username: str, gmail_id: str, password: str):
#     user = User(username="admin1", gmail_id="abcd@gmail.com", password="123456789")
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     print("Data is added to database")
#     return user


# def show_data():
#     users = db.query(User).all()
#     for u in users:
#         print(u.id, u.username, u.gmail_id, u.is_admin, u.created_at)
#     db.close()


# def check_email(email: str) -> bool:
#     user = db.query(User).filter(User.gmail_id == email).first()
#     return user.gmail_id


# def show_table():

#     inspector = inspect(engine)
#     print(inspector.get_table_names())


# if __name__ == "__main__":
#     show_data()
#     # email = "sonishubham2888@gmail.com  "
#     # show_table()
#     # import os

#     # print(os.path.abspath("try.db"))


import json
