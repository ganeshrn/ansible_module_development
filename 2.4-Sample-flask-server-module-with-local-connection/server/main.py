from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity

USER_DATA = {
    'user1': 'Secr3tPassw0rd',
}

class User():
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id=%s)" % self.id

def verify(username, password):
    print(username, password)
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return User(id=123)

def identity(payload):
    user_id = payload['identity']
    return {'user_id': user_id}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app, prefix='/api/v1')

jwt = JWT(app, verify, identity)

class PrivateResource(Resource):
    @jwt_required()
    def get(self):
        return dict(current_identity)

class Logout(Resource):
    @jwt_required()
    def get():
        return jsonify({"msg": "Successfully logged out"}), 200

api.add_resource(PrivateResource, '/private')
api.add_resource(Logout, '/logout')


if __name__ == "__main__":
    app.run(debug=True, port=8042)
