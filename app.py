from conexion import app
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surnames = db.Column(db.String(20),nullable=False)
    phone = db.Column(db.Integer, default=0)

    def __init__(self, name, surnames, phone):
        self.name = name
        self.surnames = surnames
        self.phone = phone

        db.create_all()

class ClientSchema(ma.Schema):
    class Meta:
            fields = ('id', 'name', 'surnames', 'phone')


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)


@app.route('/clients', methods=['POST'])
def createClient():
    name = request.json['name']
    surnames = request.json['surnames']
    phone = request.json['phone']

    client = Client(name, surnames, phone)
    db.session.add(client)
    db.session.commit()

    return jsonify({
        "message" : "Datos registrados correctamente!!"
    })


@app.route('/clients/<id>', methods=['PUT'])
def updateClient(id):
    client = Client.query.get(id)

    name = request.json['name']
    surnames = request.json['surnames']
    phone = request.json['phone']

    client.name = name
    client.surnames = surnames
    client.phone = phone

    db.session.commit()

    return jsonify({
        "message" : "Datos Actualizados!!"
    })


@app.route('/clients/<id>', methods=['DELETE'])
def deleteClient(id):
    client = Client.query.get(id)
    db.session.delete(client)
    db.session.commit()

    return jsonify({
        "message" : "Eliminado correctamenete!!"
    })


@app.route('/clients', methods=['GET'])
def getClients():
    clients = Client.query.all()
    result = clients_schema.dump(clients)

    return jsonify({
        "data": result
    })


@app.route('/clients/<id>', methods=['GET'])
def getClient(id):
    client = Client.query.get(id)

    if client:
        return client_schema.jsonify(client)
    else:
        return {'message': 'No existe el cliente'}
    

if __name__ == "__main__":
    app.run(debug=True)
