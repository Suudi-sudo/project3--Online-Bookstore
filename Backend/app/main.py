from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Book, Order
from pydantic import BaseModel
from typing import List

# FastAPI app
app = FastAPI()

# CORS setup
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Database setup
DATABASE_URL = "sqlite:///./bookstore.sqlite"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure database tables are created
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class UserBase(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True  


class BookBase(BaseModel):
    title: str
    author: str
    price: float
    image_url: str
    description: str
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: int
    book_id: int
    quantity: int

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int


class BookResponse(BookBase):
    id: int


class OrderResponse(OrderBase):
    id: int


# Routes

# User Endpoints
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Fetch the existing user by ID
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Delete the user
    db.delete(db_user)
    db.commit()
    return {"detail": f"User with ID {user_id} has been deleted"}


# Book Endpoints
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookBase, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author=book.author, price=book.price, image_url=book.image_url, description=book.description)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookBase, db: Session = Depends(get_db)):
    # Fetch the existing book by ID
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Update the fields if provided
    db_book.title = book.title or db_book.title
    db_book.author = book.author or db_book.author
    db_book.price = book.price or db_book.price
    db_book.image_url = book.image_url or db_book.image_url
    db_book.description = book.description or db_book.description
    db.commit()
    db.refresh(db_book)  # Refresh the object with the new values
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # Fetch the existing book by ID
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Delete the book
    db.delete(db_book)
    db.commit()
    return {"detail": f"Book with ID {book_id} has been deleted"}


# Order Endpoints
@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderBase, db: Session = Depends(get_db)):
    db_order = Order(user_id=order.user_id, book_id=order.book_id, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    # Fetch the existing order by ID
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    # Delete the order
    db.delete(db_order)
    db.commit()
    return {"detail": f"Order with ID {order_id} has been deleted"}

