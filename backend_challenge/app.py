# dependencies ------------>
from sqlalchemy import Column, Integer, String, Double, Date, ForeignKey, create_engine, select, update, delete
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from chalice import Chalice, Response
from json import dumps
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
    # save the json body in a dictionary
    body = app.current_request.json_body

    # create
    if app.current_request.method == 'POST':
        # return error if no json body is provided
        if body == None or len(body) == 0:
            return Response('No body provided', status_code=406)
        # verify if the required elements are present in the body json
        if not 'name' in body:
            return Response("Body needs 'name' element", status_code=406)
        # initialize UnitMeasure object with body data and add it to the db
        um = UnitMeasures(name=body['name'])
        with Session() as session:
            session.add(um)
            session.commit()
        return Response("UnitMeasure created successfully", status_code=201)
    
    # get
    elif app.current_request.method == 'GET':
        # get all rows if no 'id' element is specified in body
        if body == None or len(body) == 0:
            with Session() as session:
                result = session.execute(select(UnitMeasures)).all()
            # serialize data into a list of dictionaries and return it
            result = [{'id': it[0].id, 'name': it[0].name} for it in result]
            result = dumps(result)
            return Response(result, status_code=200)
        # check if 'id' element is contained in the body
        if not 'id' in body:
            return Response("Body needs 'id' element", status_code=406)
        # get the specified row
        with Session() as session:
            result = session.execute(select(UnitMeasures).where(UnitMeasures.id == body['id'])).fetchone()
        # if element does not exist in the db
        if result == None:
            return Response("Element not found", status_code=404)
        result = dumps({"id": result[0].id, "name": result[0].name})
        return Response(result, status_code=200)

    # update
    elif app.current_request.method == 'PUT':
        # return error if no json body is provided
        if body == None or len(body) == 0:
            return Response('No body provided', status_code=406)
        # verify if the required elements are present in the body json
        if not ('id' in body and 'name' in body):
            return Response("Body needs 'id' and 'name' elements", status_code=406)
        # update specified row
        with Session() as session:
            # check if row exists in the db
            if session.execute(select(UnitMeasures).where(UnitMeasures.id == body['id'])).fetchone() == None:
                return Response("Element does not exist", status_code=404)
            # update the row
            session.execute(update(UnitMeasures).where(UnitMeasures.id == body['id']).values(name=body['name']))
            session.commit()
        return Response("UnitMeasure updated successfully", status_code=201)
    
    # delete
    elif app.current_request.method == 'DELETE':
        # return error if no json body is provided
        if body == None or len(body) == 0:
            return Response('No body provided', status_code=406)
        # verify if the required elements are present in the body json
        if not 'id' in body:
            return Response("Body needs 'id'element", status_code=406)
        # delete specified row
        with Session() as session:
            # check if row exists in the db
            if session.execute(select(UnitMeasures).where(UnitMeasures.id == body['id'])).fetchone() == None:
                return Response("Element does not exist", status_code=404)
            # delete the row
            session.execute(delete(UnitMeasures).where(UnitMeasures.id == body['id']))
            session.commit()
        return Response("UnitMeasure deleted successfully", status_code=201)

@app.route('/products', methods=['POST','GET','PUT','DELETE'])
def products_endpoint():
    pass

@app.route('/sales', methods=['POST','GET'])
def sales_endpoint():
    pass