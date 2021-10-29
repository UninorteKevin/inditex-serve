from enum import unique
from re import S
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement = True)
    code = db.Column(db.String(15), primary_key = True)
    username = db.Column(db.String(50), nullable=False, unique = True)
    names = db.Column(db.String(80), nullable = False)
    surnames = db.Column(db.String(80), nullable = True)
    fecha_nacimiento = db.Column(db.DateTime(), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    status = db.Column(db.String(2), nullable = False, default = 'A')
    role = db.Column(db.String(15), nullable = False, default = 'USER') 
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    @classmethod
    def create(cls, code, username, names, surnames, fecha_nacimiento, email, password, status, role):
            user = User(code = code,
                        username = username,
                        names = names,
                        surnames = surnames,
                        fecha_nacimiento = fecha_nacimiento,
                        email = email,
                        password = password,
                        status = status,
                        role = role)
            return user.save()

    def save(self):
            try:
                    db.session.add(self)
                    db.session.commit()
                    return self
            except Exception as e:
                    db.session.rollback()
                    return None
    
    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'username': self.username,
            'names': self.names,
            'surnames': self.surnames,
            'fecha_nacimiento': self.fecha_nacimiento,
            'email': self.email,
            'password': self.password,
            'status': self.status,
            'role': self.role,
            'created_at': self.created_at
        }

#Modelo de categorias
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, autoincrement = True)
    code = db.Column(db.String(8), primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default = 0) 
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    product = relationship("Product", backref="categories")

    @classmethod
    def create(cls, code, name, quantity):
            category = Category(code = code, name = name, quantity = quantity)
            return category.save()

    def save(self):
            try:
                    db.session.add(self)
                    
                    myResponse = {
                        'status':'SUCCESS',
                        'code':200,
                        'message': 'Usuario registrado correctamente',
                        'category': Category.json(self)
                    }
                    
                    db.session.commit()
            except Exception as e:
                db.session.rollback
                myResponse = {
                    'status':'ERROR',
                    'code': 500,
                    'message': 'Error en el servidor al procesar los datos de la categoria.',
                    'define_error': e.args[0]
                }
            
            return myResponse
    
    
    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'username': self.username,
            'created_at': self.created_at
        }


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, autoincrement = True)
    code = db.Column(db.String(8), primary_key = True, nullable = False)
    reference = db.Column(db.String(25), nullable = False)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(255), nullable = True, default = 'Sin descripcion...')
    price = db.Column(db.Float, nullable = False)
    stock = db.Column(db.Integer, nullable = False)
    rate = db.Column(db.Integer, nullable = False, default = 0)
    cod_category = db.Column(db.String(8), ForeignKey("categories.code"), nullable = False)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    @classmethod
    def create(cls,code, reference, name, description, price, stock, rate, cod_category):
        product = Product(
                code = code,
                reference = reference,
                name = name,
                description = description,
                price = price,
                stock = stock,
                rate = rate,
                cod_category = cod_category
            )
        return product.save()

    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            return None

    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'reference': self.reference,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'rate' : self.rate,
            'created_at': self.created_at
        }