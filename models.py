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

class Stock(Base):
    __tablename__ = 'Stock'
    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('Book.id'))
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('Shop.id'))
    count = sq.Column(sq.Integer, nullable=False)
    stock_rel = relationship('Sale', backref='stock')

    def __str__(self):
        return {Stock.id}

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

    def __str__(self):
        return f'Sale {self.id} | {self.id_stock} | {self.date_sale} | '
    
def create_tables(eng):
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)