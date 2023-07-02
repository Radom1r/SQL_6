import os
import json
import datetime
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import *

def fill_the_tables(file):
    with open(file) as path:
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
            
def get_shops(author_name_or_id):
    resp = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if author_name_or_id.isdigit():
        resp = resp.filter(author_name_or_id == Publisher.id)
    else:
        resp = resp.filter(author_name_or_id == Publisher.name)
    session.commit()
    for tit, nam, pr, date in resp:
        print(f'{tit} | {nam} | {pr} | {date.strftime("%d-%m-%Y")}')

if __name__ == '__main__':
    DNS = 'postgresql://appadmin:jdfh8jhtghnjkfrvhyu@localhost:5432/SQL_5'
    engine = sq.create_engine(DNS)
    Session = sessionmaker(bind=engine)
    session = Session()
    create_tables(engine)
    fill_the_tables('text_data.json')
    input_id = str(input("Enter publisher's name or id: "))
    get_shops(input_id)
    session.close()