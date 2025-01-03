from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json

pymysql.install_as_MySQLdb()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

USER = 'root'
PASSWORD = ''
HOST = 'localhost'
DATABASE = 'test'
# SOCKET = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
# CONNECTION_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}?unix_socket={SOCKET}"
CONNECTION_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"

app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    description = db.Column(db.String(255))

class Transaction(Resource):
    def get(self):
        transactions = TransactionModel.query.all()
        data = [{'id': transaction.id, 'date': transaction.date, 'amount': transaction.amount, 'category': transaction.category, 'description': transaction.description} for transaction in transactions]
        return jsonify({'transactions': data, 'Method': 'GET'})

    def post(self):
        data = request.get_json()
        new_transaction = TransactionModel(date=data['date'], amount=data['amount'], category=data['category'], description=data['description'])
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'Method': 'POST', 'message': 'New transaction created successfully'})

    def put(self, id):
        data = request.get_json()
        transaction = TransactionModel.query.get(id)
        if transaction:
            transaction.date = data['date']
            transaction.amount = data['amount']
            transaction.category = data['category']
            transaction.description = data['description']
            db.session.commit()
            return jsonify({'Method': 'PUT', 'message': 'Transaction updated successfully'})
        return jsonify({'Method': 'PUT', 'message': 'Transaction not found'})

    def delete(self, id):
        transaction = TransactionModel.query.get(id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            return jsonify({'Method': 'DELETE', 'message': 'Transaction deleted successfully'})
        return jsonify({'Method': 'DELETE', 'message': 'Transaction not found'})

api.add_resource(Transaction, '/api/transactions', '/api/transactions/<int:id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)