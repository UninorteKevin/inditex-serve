from flask import Flask, request
from flask import json
from flask.json import jsonify
from models import Product, db
from config import config

from models import User, Category
def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

enviroment = config['development']
app = create_app(enviroment)

@app.route('/api/users/add', methods = ['POST'])
def addUser():
    
    try:
        new_user = User.create(request.json['code'], 
                                request.json['username'],
                                request.json['names'],
                                request.json['surname'],
                                request.json['fecha_nacimiento'],
                                request.json['email'],
                                request.json['password'],
                                request.json['status'],
                                request.json['role'])
        
        myResponse = {
            'status': 'SUCCESS',
            'code': 200,
            'message': 'Usuario creado correctamente. ',
            'user': User.json(new_user)
        }
    except Exception as e:
        myResponse = {
            'status': 'WARNING',
            'code': 202,
            'message': 'No se pudo registrar el usuario. Verifique la informacion registrada.'
        }

    return jsonify(myResponse)

@app.route('/api/users/list')
def getUsers():
    try:
        users = [ user.json() for user in User.query.all() ]
        myResponse = {
            'status': 'SUCCESS',
            'code': 200,
            'users':users
        }
    except Exception as e:
        myResponse = {
            'status': 'WARNING',
            'code': 202,
            'message': 'No se pudo registrar el usuario. Verifique la informacion registrada.',
            'define_error': e.args[0]
        }
    
    return myResponse

@app.route('/api/users/<code>', methods = ['GET'])
def getUser(code):
    try:
        user = User.query.filter_by(code=code).first()

        if(user is None):
            myResponse = {
                'status': 'WARNING',
                'code': 202,
                'message': 'No existe un usuario con el ID especificado.',
                'define_error': 'Usuario no registrado en el sistema.'
            }
        else:
            myResponse = {
                'status': 'SUCCESS',
                'code': 200,
                'user': User.json(user)
            }
        
    except Exception as e:
        myResponse = {
            'status': 'WARNING',
            'code': 202,
            'message': 'No se pudo registrar el usuario. Verifique la informacion registrada.',
            'define_error': e.args[0]
        }
    
    return myResponse


@app.route('/api/categories/add', methods = ['POST'])
def addCategory():
    code = request.json['code']
    name = request.json['name']
    quantity = request.json['quantity']

    myResponse = Category.create(code, name, quantity)

@app.route('/api/products/add', methods = ['POST'])
def addProduct():
    try:
        new_product = Product.create(
            request.json['code'],
            request.json['reference'],
            request.json['name'],
            request.json['description'],
            request.json['price'],
            request.json['stock'],
            request.json['rate'],
            request.json['cod_category']
        )
        myResponse = {
            'status': 'SUCCESS',
            'code': 200,
            'message': 'Se ha registrado el producto correctamente.',
            'product': Product.json(new_product)
        }   
    except Exception as e:
        myResponse = {
            'status': 'WARNING',
            'code': 202,
            'message': 'No se pudo registrar el producto. Verifique sus datos.',
            'define_error': e.args[0]
        }
    return jsonify(myResponse)

@app.route('/api/products/list', methods = ['GET'])
def getProducts():
    try:
        products = [ product.json() for product in Product.query.all() ]
        if(products is None):
            myResponse = {
                'status': 'WARNING',
                'code': 202,
                'message': 'No existen productos en el sistema.',
                'define_error': 'No se encontraron registro.'
            }
        else:
            myResponse = {
                'status': 'SUCCESS',
                'code': 200,
                'products': products
            }
    except Exception as e:
        myResponse = {
            'status': 'ERROR',
            'code': 500,
            'message': 'Error en la peticion al consultar los productos.',
            'define_error': e.args[0]
        }
    return myResponse

@app.route('/api/products/<code>', methods = ['GET'])
def getProduct(code):
    try:
        product = Product.query.filter_by(code=code).first()
        if(product is None):
            myResponse = {
                'status': 'WARNING',
                'code': 202,
                'message': 'No existe ningun producto en el sistema con el ID ingresado.',
                'define_error': 'No se encontraron registro.'
            }
        else:
            myResponse = {
                'status': 'SUCCESS',
                'code': 200,
                'product': Product.json(product)
            }
    except Exception as e:
        myResponse = {
            'status': 'ERROR',
            'code': 500,
            'message': 'Error en la peticion al consultar un producto.',
            'define_error': e.args[0]
        }
    return myResponse


if __name__ == "__main__":
        app.run(debug=True)



