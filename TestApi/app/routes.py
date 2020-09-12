from flask import request
from app import app, db, bcrypt, api
from app.models import Users
from flask_login import current_user, login_user, login_required, logout_user
from flask_restful import Resource, abort, fields, marshal_with

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'password': fields.String
}

def hash_password(password):
    new_password = bcrypt.generate_password_hash(password).decode('utf-8')
    return new_password

def check_password(user_password, form_password):
    checked_password = bcrypt.check_password_hash(user_password, form_password)
    return checked_password

def check_user(username):
    user = Users.query.filter_by(username=username).first()
    return user

class User(Resource):
    @marshal_with(user_fields)
    def put(self):
        if current_user.is_authenticated:
            abort(404, message="Logout first to view this page")
        args = request.get_json()
        user = check_user(args['username'])
        if user:
            abort(404, message="User already exist")
        new_user = Users(username=args['username'], password=hash_password(args['password']))
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

    @marshal_with(user_fields)
    def post(self):
        if current_user.is_authenticated:
            abort(404, message='already authenticated')
        args = request.get_json()
        user = check_user(args['username'])
        if user and check_password(user.password, args['password']):
            login_user(user, remember=True)
            print(current_user)
            return current_user
        abort(404, message="User does not exist")

    @marshal_with(user_fields)
    @login_required
    def get(self):
        return current_user

class Logout(Resource):
    def get(self):
        if current_user.is_authenticated:
            logout_user()
            return {'message':'logout successful'}
        abort(404, message="Not yet logged in")


api.add_resource(User, "/user")
api.add_resource(Logout, "/logout")