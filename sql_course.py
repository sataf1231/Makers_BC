from enum import unique
import json
from tokenize import String
import requests
from flask import Flask, Request, Response, jsonify, request
import base64
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:0257@localhost:5432/sql_course'

course_user = db.Table('course_user',
	db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_category = db.Column(db.String(20), nullable=False)
	catecourse = db.relationship('Course', backref='catecourse')

	def __repr__(self):
		return f'Category: <{self.name}>'

class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_course = db.Column(db.String(20), nullable=False)
	desc = db.Column(db.String(100), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	instructure_id = db.Column(db.Integer, db.ForeignKey('instructure.id'), nullable=False)
	# courseuser = db.relationship('User', backref='courseuser')

	def __repr__(self):
		return f'Course: <{self.name}>'

class Instructure(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_instructure = db.Column(db.String(20), nullable=False)
	username = db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(20), nullable=False)
	instcourse = db.relationship('Course', backref='instcourse')

	def __repr__(self):
		return f'Instructure: <{self.name}>'

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_user = db.Column(db.String(20), nullable=False)
	username = db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(20), nullable=False)
	# usercourse = db.relationship('Course', backref='usercourse')

	def __repr__(self):
		return f'User: <{self.name}>'

# db.create_all()
# db.session.commit()

#----------------Category------------------
#Get
@app.route('/category/')
def get_category():
	return jsonify([
			{
				'id': c.id, 'name': c.name_category
				} for c in Category.query.all()
		])
#Get id
@app.route('/category/<id>/')
def get_category_id(id):
		print(id)
		category = Category.query.filter_by(id=id).first_or_404()
		return {
			'id': category.id, 'name': category.name_category
		}, 201
#Insert
@app.route('/category/', methods=['POST'])
def create_category():
		data = request.get_json()
		if not 'name_category' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name not given'
			}), 400
		c = Category( 
				name_category=data['name_category'] 
			)
		db.session.add(c)
		db.session.commit()
		return {
			'id': c.id, 
			'name': c.name_category,
		}, 201
#Update Data
@app.route('/category/<id>/', methods=['PUT'])
def update_category(id):
	data = request.get_json()
	if 'name_category' not in data:
		return {
			'error': 'Bad Request',
			'message': 'Name field needs to be present'
		}, 400
	c = Category.query.filter_by(id=id).first_or_404()
	c.name_category=data['name_category']
	db.session.commit()
	return jsonify({
		'id': c.id, 'category name': c.name_category
		})
#Delete
@app.route('/category/<id>/', methods=['DELETE'] )
def delete_category(id):
		c = Category.query.filter_by(id=id).first_or_404()
		db.session.delete(c)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}

#------------------User-------------------
#Get
@app.route('/user/')
def get_user():
	return jsonify([
			{
				'id': i.id, 'name': i.name_user, 'username':i.username, 'password':i.password
				} for i in User.query.all()
		])
#Get id
@app.route('/user/<id>/')
def get_user_id(id):
		user = User.query.filter_by(id=id).first_or_404()
		return {
			'id': user.id, 'name': user.name_user, 'username':user.username, 'password':user.password
		}, 201
#Insert
@app.route('/user/', methods=['POST'])
def create_user():
		data = request.get_json()
		if not 'name_user' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name not given'
			}), 400
		u = User(
				name_user=data['name_user'],
				username=data['username'],
				password=data['password']
			)
		db.session.add(u)
		db.session.commit()
		return {
			'id': u.id, 
			'name_user': u.name_user,
			'username':u.username,
			'password':u.password,
		}, 201
#Update Data
@app.route('/user/<id>/', methods=['PUT'])
def update_user(id):
	data = request.get_json()
	if 'name_user' not in data:
		return {
			'error': 'Bad Request',
			'message': 'Name field needs to be present'
		}, 400
	u = User.query.filter_by(id=id).first_or_404()
	u.name_user=data['name_user']
	u.username=data['username']
	u.password=data['password']
	db.session.commit()
	return jsonify({
		'id': u.id, 'name': u.name_user, 'username':u.username,'password':u.password
		})
#Delete
@app.route('/user/<id>/', methods=['DELETE'] )
def delete_user(id):
		u = User.query.filter_by(id=id).first_or_404()
		db.session.delete(u)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
#-------------Instruktur----------------------
#Get
@app.route('/instructure/')
def get_instructure():
	return jsonify([
			{
				'id': i.id, 'name': i.name_instructure, 'username':i.username, 'password':i.password
				} for i in Instructure.query.all()
		])
#Get id
@app.route('/instructure/<id>/')
def get_user_instructure(id):
		i = Instructure.query.filter_by(id=id).first_or_404()
		return {
			'id': i.id, 'name': i.name_instructure, 'username':i.username, 'password':i.password
		}, 201
#Insert
@app.route('/instructure/', methods=['POST'])
def create_instruture():
		data = request.get_json()
		if not 'name_instructure' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name not given'
			}), 400
		ins = Instructure( 
				name_instructure=data['name_instructure'],
				username=data['username'],
				password=data['password']
			)
		db.session.add(ins)
		db.session.commit()
		return {
			'id': ins.id, 
			'name': ins.name_instructure,
			'username': ins.username,
			'password': ins.password
		}, 201
#Update Data
@app.route('/instructure/<id>/', methods=['PUT'])
def update_instructure(id):
	data = request.get_json()
	if 'name_instructure' not in data:
		return {
			'error': 'Bad Request',
			'message': 'Name field needs to be present'
		}, 400
	i = Instructure.query.filter_by(id=id).first_or_404()
	i.name_instructure=data['name_instructure']
	i.username=data['username']
	i.password=data['password']
	db.session.commit()
	return jsonify({
		'id': i.id, 'name': i.name_instructure, 'username':i.username,'password':i.password
		})
#Delete
@app.route('/instructure/<id>/', methods=['DELETE'] )
def delete_instructure(id):
		i = Instructure.query.filter_by(id=id).first_or_404()
		db.session.delete(i)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
#-------------Course----------------------
#Get
@app.route('/course/')
def get_course():
	return jsonify([
			{
				'course id': c.id, 
				'name': c.name_course, 
				'desc':c.desc, 
				'instructure':{
					"instructure name": c.instcourse.name_instructure
				},
				'category':{
					"category name": c.catecourse.name_category
				}
				} for c in Course.query.all()
		])
#Get ID
@app.route('/course/<id>/')
def get_course_id(id):
	c = Course.query.filter_by(id=id).first_or_404()
	return jsonify([
			{
				'course id': c.id, 
				'name': c.name_course, 
				'desc':c.desc, 
				'instructure':{
					"instructure name": c.instcourse.name_instructure
				},
				'category':{
					"category name": c.catecourse.name_category
				}
				} 
		])
#Insert
@app.route('/course/', methods=['POST'])
def create_course():
		data = request.get_json()
		if not 'name_course' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name not given'
			}), 400
		cate = Category.query.filter_by(name_category=data['name_category']).first()
		instruc = Instructure.query.filter_by(name_instructure=data['name_instructure']).first()
		c = Course(
				name_course=data['name_course'], 
				desc=data['desc'], 
				category_id=cate.id,
				instructure_id=instruc.id
			)
		db.session.add(c)
		db.session.commit()
		return{
			'name':c.name_course,
			'description':c.desc,
			'category':c.category_id,
			'instrcture':c.instructure_id
		}
#Update Data
@app.route('/course/<id>/', methods=['PUT'])
def update_course(id):
	data = request.get_json()
	if 'name_course' not in data:
		return {
			'error': 'Bad Request',
			'message': 'Name field needs to be present'
		}, 400
	cate = Category.query.filter_by(id=id).first()
	inst = Instructure.query.filter_by(id=id).first()
	course = Course.query.filter_by(id=id).first_or_404()
	course.name_course=data['name_course']
	course.desc=data['desc']
	db.session.commit()
	return{
		'message':'Success'
	}
	# return jsonify({
	# 	'name':course.name_course,
	# 	'description':course.desc,
	# 	'category':cate.name_category,
	# 	'instructure':inst.name_instructure
	# 	})
#Delete
@app.route('/course/<id>/', methods=['DELETE'] )
def delete_course(id):
		c = Course.query.filter_by(id=id).first_or_404()
		db.session.delete(c)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
