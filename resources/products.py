from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from services.open_food_fact import open_food_fact
from database.models import db, Product, Purchase
import json


class ProductAPI(Resource):
    @jwt_required()
    def get(self, bar_code):
        data = open_food_fact.get_product_by_code(bar_code)
        product = Product.query.filter_by(bar_code = bar_code).first()
        
        if not product:
            data = open_food_fact.get_product_by_code(bar_code)
            product = Product(
                bar_code = bar_code,
                name = data['product']['product_name'],
                nutri_score = data['product']['nutriscore_grade'],
                brand = data['product']['brands']
            )
            try:
                db.session.add(product)
                db.session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Couldnt add product because : %s' % e}, 400    
        
        try:
            return(json.loads('{"name":"'+ data['product']['product_name'] + '", "brand": "' 
                          + data['product']['brands']+ '", "nutri_score":"'+ data['product']['nutriscore_grade']+ '"}'))
        except Exception as e:
            print(e)
            return {'error': 'Couldnt get the product because : %s' % e}, 400        
        

    
class ProductsAPI(Resource):
    @jwt_required()
    def get(self):
        users = Product.query.all()
        return jsonify(users)


class ProductBuyAPI(Resource):
    @jwt_required()
    def post(self):
        body = request.get_json()
        bar_code = body.get('bar_code')
        
        product = Product.query.filter_by(bar_code = bar_code).all()
        if not product:
            data = open_food_fact.get_product_by_code(bar_code)
            product = Product(bar_code=bar_code,name=data['product']['product_name'],
                nutri_score=data['product']['nutriscore_grade'],
                brand=data['product']['brands'])
            db.session.add(product)
            db.session.commit() 
            
        purchase = Purchase(
            bar_code = bar_code,
            price = body.get('price'),
            user_id = get_jwt_identity()
        )
        
        try:
            db.session.add(purchase)
            db.session.commit() 
            return jsonify(purchase)
        except Exception as e:
            print(e)
            return {'error': 'Couldnt add purchase because : %s' % e}, 400