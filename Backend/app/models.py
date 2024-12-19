from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()
# Book Model
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    price = Column(Float)
    image_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
# User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# Order Model
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    quantity = Column(Integer)

    user = relationship("User", back_populates="orders")
    book = relationship("Book", back_populates="orders")

# Add relationships to models for ease of access
User.orders = relationship("Order", back_populates="user")
Book.orders = relationship("Order", back_populates="book")