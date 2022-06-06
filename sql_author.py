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
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:0257@localhost:5432/sql_perpus' 

penulis_buku = db.Table('penulis_buku',
    db.Column('buku_id', db.String(5), db.ForeignKey('buku.id_buku'), primary_key=True),
    db.Column('penulis_id', db.String(5), db.ForeignKey('penulis.id_penulis'), primary_key=True)
)

class Kategori(db.Model):
	id_kategori = db.Column(db.String(5), primary_key=True)
	genre = db.Column(db.String(20), nullable=False)
	bukus = db.relationship('Buku', backref='category', lazy='dynamic')
	
	def __repr__(self):
		return f'Kategori: <{self.genre}>'

class Buku(db.Model):
	id_buku = db.Column(db.String(5), primary_key=True)
	judul = db.Column(db.String(50), nullable=False)
	jml_halaman = db.Column(db.Integer, default=False)
	thn_rilis = db.Column(db.Integer, nullable=False)
	kuantitas = db.Column(db.Integer, nullable=False)
	kategori_id = db.Column(db.String(5), db.ForeignKey('kategori.id_kategori'), nullable=False)
	buku_penulis = db.relationship('Penulis',backref='author_book', secondary='penulis_buku')
	
	def __repr__(self):
		return f'Buku: <{self.judul}>'

class Penulis(db.Model):
	id_penulis = db.Column(db.String(5), primary_key=True, index=True)
	nama_penulis = db.Column(db.String(20), nullable=False)
	authors = db.relationship('Buku', backref='authors', secondary='penulis_buku')
	
	def __repr__(self):
		return f'Penulis: <{self.nama_penulis}>'


class User(db.Model):
	id_user = db.Column(db.Integer, primary_key=True, index=True)
	name = db.Column(db.String(20), nullable=False)
	username = db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(20), nullable=False, unique=True)
	is_admin = db.Column(db.Boolean, default=False)
	# rents = db.relationship('Peminjaman', backref='rent', lazy='dynamic')

	def __repr__(self):
		return f'User <{self.name}>'

class Peminjaman(db.Model):
	id_peminjaman = db.Column(db.Integer, primary_key=True, index=True)
	tgl_pinjam = db.Column(db.Date, nullable=False)
	tgl_kembali = db.Column(db.Date, nullable=False)
	buku_id = db.Column(db.String(5), db.ForeignKey('buku.id_buku'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
	admin_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
	book = db.relationship('Buku', backref='book', lazy=True)

	def __repr__(self):
		return f'Peminjaman <{self.tgl_pinjam}>'

# db.create_all()
# db.session.commit()

@app.route('/')
def home():
	return {
		'message': 'Welcome Library'
	}

# @app.route('/auth/')
def auth(a):
	# a = request.headers.get('Authorization')
	b = base64.b64decode(a[6:])
	c = b.decode("ascii")
	lis = c.split(':')
	username = lis[0]
	passwords = lis[1]
	user = User.query.filter_by(username=username).filter_by(password=passwords).first()
	if not user:
		return 'Check your login details.'
	elif not user.is_admin:
		return False
	elif user.is_admin == True:
		return True

def auth_admin(auth):
    # decode_var = request.headers.get('Authorization')
    c = base64.b64decode(auth[6:])
    e = c.decode("ascii")
    lis = e.split(':')
    username = lis[0]
    passw = lis [1]

    return [username, passw]

#------------Kategori-------------
#Get Data
@app.route('/kategori/')
def get_kategori():
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True or False:
		return jsonify([
			{
				'id': kategori.id_kategori, 'genre': kategori.genre
				} for kategori in Kategori.query.all()
		])
	else:
		return{
		 'message':'Access Failed'
	},401

#Insert Data
@app.route('/kategori/', methods=['POST'])
def create_kategori():
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		data = request.get_json()
		if not 'genre' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name not given'
			}), 400
		k = Kategori(
				id_kategori=data['id_kategori'], 
				genre=data['genre'] 
			)
		db.session.add(k)
		db.session.commit()
		return {
			'id': k.id_kategori, 'genre': k.genre
		}, 201
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#Update Data
@app.route('/kategori/<id>/', methods=['PUT'])
def update_kategori(id):
	data = request.get_json()
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		if 'genre' not in data:
			return {
				'error': 'Bad Request',
				'message': 'Name field needs to be present'
			}, 400
		k = Kategori.query.filter_by(id_kategori=id).first_or_404()
		k.id_kategori=data['id_kategori']
		k.genre=data['genre']
		db.session.commit()
		return jsonify({
			'id': k.id_kategori, 'genre': k.genre
			})
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#Delete Data
@app.route('/kategori/<id>/', methods=['DELETE'] )
def delete_kategori(id):
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		k = Kategori.query.filter_by(id_kategori=id).first_or_404()
		db.session.delete(k)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#---------------Penulis-------------------------------
#Get Data
@app.route('/penulis/')
def get_penulis():
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True or False:
		return jsonify([
			{
				'id': penulis.id_penulis, 'nama': penulis.nama_penulis
				} for penulis in Penulis.query.all()
		])
	else:
		return{
		 'message':'Access Failed'
	},401

#Insert Data
@app.route('/penulis/', methods=['POST'])
def create_penulis():
	data = request.get_json()
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		if not 'nama_penulis' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name not given'
			}), 400
		p = Penulis(
				id_penulis=data['id_penulis'], 
				nama_penulis=data['nama_penulis'] 
			)
		db.session.add(p)
		db.session.commit()
		return {
			'id': p.id_penulis, 'nama': p.nama_penulis
		}, 201
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#Update Data
@app.route('/penulis/<id>/', methods=['PUT'])
def update_penulis(id):
	data = request.get_json()
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		if 'nama_penulis' not in data:
			return {
				'error': 'Bad Request',
				'message': 'Name field needs to be present'
			}, 400
		p = Penulis.query.filter_by(id_penulis=id).first_or_404()
		p.id_penulis=data['id_penulis']
		p.nama_penulis=data['nama_penulis']
		db.session.commit()
		return jsonify({
			'id': p.id_penulis, 'nama': p.nama_penulis
			})
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#Delete Data
@app.route('/penulis/<id>/', methods=['DELETE'] )
def delete_penulis(id):
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		p = Penulis.query.filter_by(id_penulis=id).first_or_404()
		db.session.delete(p)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#------------------Buku------------------------------
#Get Data
@app.route('/buku/')
def get_buku():
	# buku = Buku.query.filter_by(id_buku).first_or_404()
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True or False:
		return jsonify([
			{
				'id': buku.id_buku, 
				'judul': buku.judul, 
				'jumlah halaman': buku.jml_halaman,
				'tahun terbit':buku.thn_rilis,
				'kuantitas': buku.kuantitas,
				'kategori':{
					'genre': buku.category.genre,
				},
				'penulis':[
					p.nama_penulis
					for p in buku.authors
				]
				} for buku in Buku.query.all()
		])
	else:
		return{
		 'message':'Access Failed'
	},401

#Get Data ID
@app.route('/buku/<id>/')
def get_buku_id(id):
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True or False:
		buku = Buku.query.filter_by(id_buku=id).first_or_404()
		return jsonify([
			{
				'id': buku.id_buku, 'judul': buku.judul, 
				'jumlah halaman': buku.jml_halaman,
				'tahun terbit':buku.thn_rilis,
				'kuantitas': buku.kuantitas,
				'kategori':{
					'genre': buku.category.genre,
				},
				'penulis':[
					p.nama_penulis
					for p in buku.authors
				]
			}	
		])
	else:
		return{
		 'message':'Access Failed'
	},401

#Insert Data
@app.route('/buku/', methods=['POST'])
def create_buku():
	data = request.get_json()
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		if not 'judul' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name not given'
			}), 400
		k = Kategori.query.filter_by(genre=data['genre']).first()
		# a = Penulis.query.filter_by(nama_penulis=data['nama_penulis']).first()
		if not k :
			return {
				'error': 'Bad Request',
				'message': 'Invalid category'
			}
		# if not a in data:
		# 	return {
		# 		'error': 'Bad Request',
		# 		'message': 'Invalid Author'
		# 	}
		b = Buku(
				id_buku=data['id_buku'], 
				judul=data['judul'],
				jml_halaman=data['jml_halaman'], 
				thn_rilis=data['thn_rilis'], 
				kuantitas=data['kuantitas'],
				kategori_id = k.id_kategori 
			)
		db.session.add(b)
		db.session.commit()
		return {
			'id': b.id_buku, 
			'judul': b.judul, 
			'jumlah halaman': data['jml_halaman'],
			'tahun terbit':data['thn_rilis'],
			'kuantitas':data['kuantitas'],
			'category':{
				'genre':b.category.genre
			}
			# 'a':[b.authors.nama_penulis]
		}, 201
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#Update Data
@app.route('/buku/<id>/', methods=['PUT'])
def update_buku(id):
	data = request.get_json()
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		if 'id_buku' not in data:
			return {
				'error': 'Bad Request',
				'message': 'Name field needs to be present'
			}, 400
		b = Buku.query.filter_by(id_buku=id).first_or_404()
		b.id_buku=data['id_buku'],
		b.judul=data['judul'],
		b.jml_halaman=data['jml_halaman']
		b.thn_rilis=data['thn_rilis']
		b.kategori_id=data['kategori_id']
		db.session.commit()
		return jsonify({
			'id': b.id_buku, 'judul': b.judul, 'jumlah halaman': b.jml_halaman, 
			'tahun rilis':b.thn_rilis, 'kategori_id':b.kategori_id
			})
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#Delete Data
@app.route('/buku/<id>/', methods=['DELETE'] )
def delete_buku(id):
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		b = Buku.query.filter_by(id_buku=id).first_or_404()
		db.session.delete(b)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#---------------Buku-Penulis----------------------------
#Get Data
@app.route('/author_book/')
def get_author_book():
	data = request.get_json()
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True or False:
		books = Buku.query.filter_by(id_buku=data['buku_id']).first_or_404()
		author = Penulis.query.filter_by(id_penulis=data['penulis_id']).first_or_404()
		return jsonify([
			{
				'id buku': books
			}
			# 'id penulis': [
			# 	author.penulis_id
			# ]
		])
	else:
		return{
		 'message':'Access Failed'
	},401

#Add Data
@app.route('/author_book/' , methods=['POST'])
def create_author_book():
	data = request.get_json()
	books = Buku.query.filter_by(id_buku=data['buku_id']).first_or_404()
	author = Penulis.query.filter_by(id_penulis=data['penulis_id']).first_or_404()
	books.buku_penulis.append(author)
	db.session.add(books)
	db.session.commit()

	return {
		"message" : "success"
	},201

#---------------------User------------------
#Get Data Per ID
@app.route('/user/')
def get_user():
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True or False:
		return jsonify([
			{
				'id': user.id_user, 
				'name': user.name, 
				'username':user.username,
				'password':user.password, 
				'is_admin':user.is_admin
				}for user in User.query.all()
		])
	else:
		return{
		 'message':'Access Failed'
	},401

#Insert data
@app.route('/user/', methods=['POST'])
def create_user():
	data = request.get_json()
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		if not 'username' in data or not 'name' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name or Username not given'
			}), 400
		if len(data['username']) < 4 :
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name and email must be contain minimum of 4 letters'
			}), 400
		u = User( 
				name=data['name'],
				username=data['username'], 
				password=data['password'], 
				is_admin=data.get('is_admin', False)
			)
		db.session.add(u)
		db.session.commit()
		return {
			'id': u.id_user, 
			'nama': u.name, 
			'username': u.username,
			'password': u.password, 
			'is_admin': u.is_admin
		}, 201
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow

#----------------------Peminjaman------------------
#Get Rent
@app.route('/peminjaman/')
def get_rent():
    return jsonify([
        {
            'id_peminjaman': rent.id_peminjaman,
            'tgl_pinjam': rent.tgl_pinjam,
            'tgl_kembali': rent.tgl_kembali,
            'user_id' : rent.user_id,
            'buku_id' : {
                "id_buku" : rent.book.id_buku,
                "judul" : rent.book.judul,
				"kuantitas": rent.book.kuantitas
            },
            'admin_id': rent.admin_id
        } for rent in Peminjaman.query.all()
    ]),200

#Insert Rent
@app.route('/peminjaman/', methods=['POST'])
def create_rent():
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		data = request.get_json()
		user = User.query.filter_by(name=data['name']).first()
		if 'name' not in data:
			return jsonify({
                'error': 'Bad Request',
                ' message': 'Name not given'
            }), 400
		for i in data['judul']:
			book = Buku.query.filter_by(judul=i).first()
			if not book:
				return jsonify({
                    'error': 'Bad Request',
                    ' message': 'Title not given'
                }), 400
			if book.kuantitas == 0:
				return jsonify({
                    'error': 'Bad Request',
                    ' message': 'Title not given'
                }), 400
			admin = auth_admin(decode)[0]
			admin_ = User.query.filter_by(username=admin).first()
			for x in data['judul']:
				book = Buku.query.filter_by(judul=x).first()
				rent = Peminjaman(
					tgl_pinjam=data['tgl_pinjam'], 
                    tgl_kembali=data['tgl_kembali'], 
                    buku_id=book.id_buku,
                    user_id=user.id_user,
                    admin_id=admin_.id_user
                )
			book.kuantitas -= 1
		db.session.add(rent)
		db.session.commit()
		return {
            "message" :  "success"
            # 'id': rent.public_id,
            # 'date rent': rent.date_rent, 
            # 'date return': rent.date_return,
            # 'user_id' : {
            #     rent.rent.user_id
            # },
            # 'book_id' : {
            #     rent.book.title
            # },
            # 'is admin': rent.rent.is_admin
        }, 201
	else:
		return{
			"message":"Access Denied"
		},401

#Update Rent
@app.route('/peminjaman/<id>/', methods=['PUT'])
def update_rent(id):
    decode_var = request.headers.get('Authorization')
    allow = auth(decode_var)
    if allow == True:
        data = request.get_json()
        rent = Peminjaman.query.filter_by(id_peminjaman=id).first_or_404()
        books = Buku.query.filter_by(id_buku=rent.buku_id).first_or_404()
        rent.tgl_kembali = data['tgl_kembali']
        books.kuantitas +=1
        db.session.commit()
        return {
            'message': 'success'
        }
    else:
        return{
            'message': 'Access denied'
        }, 401

#Delete Data
@app.route('/peminjaman/', methods=['DELETE'] )
def delete_rent(id):
	decode = request.headers.get('Authorization')
	allow = auth(decode)
	if allow == True:
		b = Buku.query.filter_by(id_peminjaman=id).first_or_404()
		db.session.delete(b)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
	elif allow == False:
		return 'Youre not Admin'
	elif allow == 'Check your login details.':
		return allow
