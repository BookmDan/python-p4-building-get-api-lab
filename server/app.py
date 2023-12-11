#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [{'id': bakery.id, 'name': bakery.name, 'location': bakery.location} for bakery in bakeries]
    return jsonify(bakery_list)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'location': bakery.location,
            'baked_goods': [{'id': good.id, 'name': good.name, 'price': good.price} for good in bakery.baked_goods]
        }
        return jsonify(bakery_data)
    return jsonify({'error': 'Bakery not found'}), 404


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods_list = [{'id': good.id, 'name': good.name, 'price': good.price} for good in baked_goods]
    return jsonify(goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive_good:
        return jsonify({'id': most_expensive_good.id,'name':most_expensive_good.name, 'price': most_expensive_good.price})
    return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
