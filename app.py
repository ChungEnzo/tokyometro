from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datademo.db'
db = SQLAlchemy(app)

class Database(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'{self.name},{self.age},{self.email},{self.address}'

taskFields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'email': fields.String,
    'address': fields.String
}

class Items(Resource):
    @marshal_with(taskFields)
    def get(self):
        tasks = Database.query.all()
        return tasks
    
    @marshal_with(taskFields)
    def post(self):
        data = request.json
        task = Database(name=data['name'], age=data['age'], email=data['email'], address=data['address'])
        db.session.add(task)
        db.session.commit()
        tasks = Database.query.all()
        # itemId = len(Data.keys()) + 1
        # Data[itemId] = {'name':data['name']}
        return tasks
    
class Item(Resource):
    @marshal_with(taskFields)
    def get(self, id):
        task = Database.query.filter_by(id=id).first()
        return task
    
    @marshal_with(taskFields)
    def put(self, id):
        data = request.json
        task = Database.query.filter_by(id=id).first()
        task.name = data['name']
        task.age = data['age']
        task.email = data['email']
        task.address = data['address']
        db.session.commit()
        # Data[id]['name'] = data['name']
        return task
    
    @marshal_with(taskFields)
    def delete(self, id):
        task = Database.query.filter_by(id=id).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Database.query.all()
        # del Data[id]
        return tasks

    
api.add_resource(Items, '/') 
api.add_resource(Item, '/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)