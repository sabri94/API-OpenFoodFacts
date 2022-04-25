from audioop import reverse
from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from services.open_food_fact import open_food_fact
from database.models import db, Product, Purchase, User
import requests
import json
import sqlalchemy
from sqlalchemy import func


class UserRankingAPI(Resource):
    @jwt_required()
    def get(self):
        query = Purchase.query.with_entities(Purchase.user_id, func.sum(Purchase.price)).group_by(Purchase.user_id).order_by(func.sum(Purchase.price).desc()).all()

        res = {}
        users_names = []
        total_prices = []
        
        for row in query:
            user_name = User.query.filter_by(id=row[0]).first().full_name
            users_names.append(user_name)
            total_prices.append(row[1])
        
        for i in range(0, len(users_names)):
            res[users_names[i]] = total_prices[i]
            
        res = dict(sorted(res.items(), key = lambda x: x[1], reverse=True))    
            
        return jsonify(res)
    

class ProductRankingAPI(Resource):
    @jwt_required()
    def get(self):
        query = Purchase.query.with_entities(Purchase.bar_code, func.count(Purchase.id)).group_by(Purchase.bar_code).all()
        
        res = {}
        products_names = []
        transactions = []
        
        for row in query:
            product_name = Product.query.filter_by(bar_code=row[0]).first().name
            products_names.append(product_name)
            transactions.append(row[1])
        
        for i in range(0, len(products_names)):
            res[products_names[i]] = transactions[i]
            
        res = dict(sorted(res.items(), key = lambda x: x[1], reverse=True))
            
        return jsonify(res)