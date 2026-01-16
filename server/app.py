#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os
from pathlib import Path

from models import db, Plant

app = Flask(__name__)
# Use an absolute path for the sqlite database file located at the repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / 'plants.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [p.to_dict() for p in plants], 200

    def post(self):
        data = request.get_json()
        p = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(p)
        db.session.commit()
        return p.to_dict(), 201


class PlantByID(Resource):
    def get(self, id):
        p = Plant.query.get_or_404(id)
        return p.to_dict(), 200
        

# register resources
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

# Ensure database and tables exist for simple test runs
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(port=5555, debug=True)
