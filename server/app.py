#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'


@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()

    response = make_response(
        bakery_serialized,
        200
    )
    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]

    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(
        BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response


@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    bakery_id = data.get('bakery_id')

    if not name or not bakery_id:
        return jsonify({"error": "Name and bakery_id required"}), 400
    bakery = Bakery.query.get(bakery_id)

    if bakery is None:
        return jsonify({"error": "Bakery with the provided ID does not exist"}), 404
    baked_good = BakedGood(name=name, bakery_id=bakery_id)
    db.session.add(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good created successfully", "data": {"id": baked_good.id, "name": baked_good.name}}), 201


@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if bakery is None:
        return jsonify({"error": "Bakery with the provided ID does not exist"}), 404

    data = request.form
    new_name = data.get('name')

    if new_name:
        bakery.name = new_name
        db.session.commit()

    return jsonify({"message": "Bakery updated successfully", "data": {"id": bakery.id, "name": bakery.name}})

# Delete Baked Good


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGoods.query.get(id)

    if baked_good is None:
        return jsonify({"error": "Baked Good with the provided ID does not exist"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked Good deleted successfully"})


if __name__ == '__main__':
    app.run(port=5555, debug=True)
