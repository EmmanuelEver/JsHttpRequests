from flask import Flask, render_template, redirect, request, url_for, make_response, abort, jsonify
from datetime import date
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "aksmdja234234eefsdfsde2"

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	password = db.Column(db.String(20), nullable = False)
	fullname = db.Column(db.String(30), nullable = False)
	job = db.Column(db.String(30), default = "not applicable", nullable = True)

	def __init__(self, username, password, fullname, job):
		self.username = username
		self.password = password
		self.fullname = fullname
		self.job = job


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def json(self):
		return {"username" : self.username, "fullname" : self.fullname, "job" : self.job}

	@classmethod
	def search(cls, username):
		user = User.query.filter_by(username = username).all()
		return user


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
	if request.get_json():
		data = request.get_json()
		user = User.search(data["username"])
		if not user:
			try:
				print("if not user flag")
				user = User(**data)
				print(user.json())
				user.save_to_db()
				res = make_response(jsonify({"msg" : "User successfully added", "user" : user.json()}),200)
				return res

			except:
				res = make_response(jsonify({"msg" : "internal server error"}),500)
				return res
		else:
			res = make_response(jsonify({"msg" : "Username already exist"}),400)
			return res
	if request.form:
		data = {
				"username" : request.form["username"],
				"password" : request.form["password"],
				"fullname" : request.form["fullname"],
				"job"	   : request.form["job"]
				}

		user = User.search(data["username"])
		if not user:
			try:
				print("if not user flag")
				user = User(**data)
				print(user.json())
				user.save_to_db()
				res = make_response(jsonify({"msg" : "User successfully added", "user" : user.json()}),200)
				return res

			except:
				res = make_response(jsonify({"msg" : "internal server error"}),500)
				return res
		else:
			res = make_response(jsonify({"msg" : "Username already exist"}),400)
			return res
	res = make_response(jsonify({"msg" : "Invalid arguments"}),400)
	print(res)
	return res


@app.route("/<username>")
def search(username):
	user = User.search(username)
	if user:
		res = make_response(jsonify(user))
		res.status_code = 200
		res.headers["Message"] = "The request is accpeted"
		return res

@app.route('/users')
def user():
	users = [user.json() for user in User.query.all()]
	res = make_response(jsonify( users))
	return res
if __name__ == "__main__":
	app.run(debug=True)