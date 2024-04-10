# dependencies ------------>
from sqlalchemy import Column, Integer, String, Double, DateTime, ForeignKey, create_engine, select, update, delete
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from chalice import Chalice, Response
from datetime import datetime
import sqlalchemy.exc
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
    date = Column(DateTime, default=datetime.now)
    # establish the relationship with Products
    products = relationship('Products', back_populates='sales')

# create tables in db
Base.metadata.create_all(engine)

# endpoints ------------>
@app.route('/unitmeasures', methods=['POST','GET','PUT','DELETE'])
def unit_measure_endpoint():
    # save the json body in a dictionary
    body = app.current_request.json_body

    # return error if no json body is provided
    if (body == None or len(body) == 0) and app.current_request.method != 'GET':
        return Response('No body provided', status_code=406)


    # create
    if app.current_request.method == 'POST':
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
        # verify if the required elements are present in the body json
        if not 'id' in body:
            return Response("Body needs 'id' element", status_code=406)
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
    # save the json body in a dictionary
    body = app.current_request.json_body

    # return error if no json body is provided
    if (body == None or len(body) == 0) and app.current_request.method != 'GET':
        return Response('No body provided', status_code=406)

    # create
    if app.current_request.method == 'POST':
        # verify if the required elements are present in the body json
        if not ('name' in body and 'price' in body and 'um_id' in body):
            return Response("Body needs 'name', 'price' and 'um_id' elements", status_code=406)
        # initialize Product object with body data and add it to the db
        pr = Products(name=body['name'], price=body['price'], um_id=body['um_id'])
        # if um_id does not exist, catch IntegrityError and return feedback to the client
        try:
            with Session() as session:
                session.add(pr)
                session.commit()
        except sqlalchemy.exc.IntegrityError:
            return Response("um_id does not exist in the db", status_code=404)
        # catch any other errors
        except:
            return Response("An error occured", status_code=500)

        return Response("Product created successfully", status_code=201)
    
    # get
    elif app.current_request.method == 'GET':
        # get all rows if no 'name' element is specified in body
        if body == None or len(body) == 0:
            with Session() as session:
                result = session.execute(select(Products)).all()
            # serialize data into a list of dictionaries and return it
            result = [{'name': it[0].name, 'price': it[0].price, 'um_id': it[0].um_id} for it in result]
            result = dumps(result)
            return Response(result, status_code=200)
        # check if 'name' element is contained in the body
        if not 'name' in body:
            return Response("Body needs 'name' element", status_code=406)
        # get the specified row
        with Session() as session:
            result = session.execute(select(Products).where(Products.name == body['name'])).fetchone()
        # if element does not exist in the db
        if result == None:
            return Response("Element not found", status_code=404)
        result = dumps({'name': result[0].name, 'price': result[0].price, 'um_id': result[0].um_id})

        return Response(result, status_code=200)

    # update
    elif app.current_request.method == 'PUT':
        # verify if the required elements are present in the body json
        if not ('name' in body and 'price' in body and 'um_id' in body):
            return Response("Body needs 'name', 'price' and 'um_id' elements", status_code=406)
            # update specified row
        with Session() as session:
            # check if row exists in the db
            if session.execute(select(Products).where(Products.name == body['name'])).fetchone() == None:
                return Response("Element does not exist", status_code=404)
            # if um_id does not exist, catch IntegrityError and return feedback to the client
            try:
                # update the row
                session.execute(update(Products).where(Products.name == body['name']).values(price=body['price'], um_id=body['um_id']))
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                return Response("um_id does not exist in the db", status_code=404)
            # catch any other errors
            except:
                return Response("An error occured", status_code=500)

        return Response("Product updated successfully", status_code=201)
    
    # delete
    elif app.current_request.method == 'DELETE':
        # verify if the required elements are present in the body json
        if not 'name' in body:
            return Response("Body needs 'name' element", status_code=406)
        # delete specified row
        with Session() as session:
            # check if row exists in the db
            if session.execute(select(Products).where(Products.name == body['name'])).fetchone() == None:
                return Response("Element does not exist", status_code=404)
            # delete the row
            session.execute(delete(Products).where(Products.name == body['name']))
            session.commit()
        return Response("Product deleted successfully", status_code=201)

@app.route('/sales', methods=['POST','GET'])
def sales_endpoint():
    # save the json body in a dictionary
    body = app.current_request.json_body

    # return error if no json body is provided
    if (body == None or len(body) == 0) and app.current_request.method != 'GET':
        return Response('No body provided', status_code=406)

    # create
    if app.current_request.method == 'POST':
        # verify if the required elements are present in the body json
        if not ('p_name' in body and 'quantity' in body):
            return Response("Body needs 'p_name' and 'quantity' elements", status_code=406)
        # initialize Sales object with body data and add it to the db
        sa = Sales(p_name=body['p_name'], quantity=body['quantity'])
        # if p_name does not exist, catch IntegrityError and return feedback to the client
        try:
            with Session() as session:
                session.add(sa)
                session.commit()
        except sqlalchemy.exc.IntegrityError:
            return Response("'p_name' does not exist in the db", status_code=404)
        # catch any other errors
        except:
            return Response("An error occured", status_code=500)

        return Response("Sale created successfully", status_code=201)
    
    # get
    elif app.current_request.method == 'GET':
        with Session() as session:
            # get all rows if no 'p_name' element is specified in body
            if body == None or len(body) == 0:
                # get all rows from sales table
                result = session.execute(select(Sales)).all()
            # check if 'p_name' element is contained in the body
            elif not 'p_name' in body:
                return Response("Body needs 'p_name' element", status_code=406) 
            else:
                result = session.execute(select(Sales).where(Sales.p_name == body['p_name'])).all()
            # if product does not exist
            if result == None or len(result) == 0:
                return Response("Element not found", status_code=404)
            sum = {}
            # obtain the sum of the quantity of units sold and earned amount for each product
            for it in result:
                # first time product is found
                if not it[0].p_name in sum:
                    # get the price of the product
                    product = session.execute(select(Products).where(Products.name == it[0].p_name)).fetchone()[0]
                    sum[it[0].p_name] = {'quantity': 0, 'amount': product.price}
                # update the quantity of sold units of the given product
                sum[it[0].p_name]['quantity'] += it[0].quantity
        # obtain the total earned amount of each product
        for it in sum.keys():
            sum[it]['amount'] = sum[it]['amount'] * sum[it]['quantity']
        # serialize sum dictionary
        sum = dumps(sum)
        return Response(sum, status_code=200)