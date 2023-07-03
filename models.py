import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'Publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)

class Book(Base):
    __tablename__ = 'Book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('Publisher.id'))
    publishers = relationship("Publisher", backref='Book')

class Stock(Base):
    __tablename__ = 'Stock'
    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('Book.id'))
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('Shop.id'))
    count = sq.Column(sq.Integer, nullable=False)
    shops = relationship("Shop", backref="Stock")
    books = relationship('Book', backref="Book")

class Shop(Base):
    __tablename__ = 'Shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)

class Sale(Base):
    __tablename__ = "Sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("Stock.id"))
    count = sq.Column(sq.Integer, nullable=False)
    stocks = relationship('Stock', backref='Sale')
    
def create_tables(eng):
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)