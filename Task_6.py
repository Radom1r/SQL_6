import os
import json
import datetime
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref

DNS = 'postgresql://appadmin:jdfh8jhtghnjkfrvhyu@localhost:5432/SQL_5'
engine = sq.create_engine(DNS)
Session = sessionmaker(bind=engine)

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
    Base.metadata.create_all(eng)

if __name__ == '__main__':
    session = Session()
    Base.metadata.drop_all(engine)
    create_tables(engine)
    with open('text_data.json') as path:
        json_file = json.load(path)
    for value in json_file:
        if value['model'] == 'publisher':
            publisher = Publisher(id=value['pk'], name=value['fields']['name'])
            session.add(publisher)
            session.commit()
        elif value['model'] == 'book':
            book = Book(id=value['pk'], title=value['fields']['title'], publisher_id=value['fields']['id_publisher'])
            session.add(book)
            session.commit()
        elif value['model'] == 'shop':
            shop = Shop(id=value['pk'], name=value['fields']['name'])
            session.add(shop)
            session.commit()
        elif value['model'] == 'stock':
            stock = Stock(id=value['pk'], shop_id=value['fields']['id_shop'], book_id=value['fields']['id_book'], count=value['fields']['count'])
            session.add(stock)
            session.commit()
        elif value['model'] == 'sale':
            sale = Sale(id=value['pk'], price=value['fields']['price'], date_sale=datetime.datetime.strptime(value['fields']['date_sale'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S"), count=value['fields']['count'], id_stock=value['fields']['id_stock'])
            session.add(sale)
            session.commit()
    session.close()