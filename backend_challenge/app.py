# dependencies ------------>
from sqlalchemy import Column, Integer, String, Double, Date, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from chalice import Chalice
import psycopg2
import os

# program variables ------------>
# chalice app instance
app = Chalice(app_name='backend_challenge')
# connection to the db
engine = create_engine(f"postgresql://{os.environ['USER']}:{os.environ['PASSWD']}@{os.environ['HOSTNAME']}/{os.environ['DB']}")
# create a session maker object and bind the engine
Session = sessionmaker(bind=engine)

# ORM Classes ------------>
# declarative base class
Base = declarative_base()

# Unit Measure mapped class
class UnitMeasures(Base):
    __tablename__ = 'unitmeasures'
    # columns
    id = Column(Integer, primary_key=True) #PK
    name = Column(String)
    # establish the relationship with Products
    products = relationship('Products', back_populates='unitmeasures')

# Products mapped class
class Products(Base):
    __tablename__ = 'products'
    # columns
    name = Column(String, primary_key=True) #PK
    price = Column(Double)
    um_id = Column(ForeignKey('unitmeasures.id')) #FK
    # establish the relationship with Products
    unitmeasures = relationship('UnitMeasures', back_populates='products')
    # establish the relationship with Sales
    sales = relationship('Sales', back_populates='products')

# Sales mapped class
class Sales(Base):
    __tablename__ = 'sales'
    # columns
    id = Column(Integer, primary_key=True) #PK
    p_name = Column(ForeignKey('products.name'))
    quantity = Column(Double)
    date = Column(Date)
    # establish the relationship with Products
    products = relationship('Products', back_populates='sales')

# create tables in db
Base.metadata.create_all(engine)

# endpoints ------------>
@app.route('/unitmeasures', methods=['POST','GET','PUT','DELETE'])
def unit_measure_endpoint():
    pass

@app.route('/products', methods=['POST','GET','PUT','DELETE'])
def products_endpoint():
    pass

@app.route('/sales', methods=['POST','GET'])
def sales_endpoint():
    pass