from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3308
mysql.init_app(app)


@app.route("/")
def main():
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
	try :
		# read the posted values from the UI
		_name = request.form['inputName'];
		_email = request.form['inputEmail'];
		_password = request.form['inputPassword'];

		# validate the received values
		if _name and _email and _password:
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_createUser',(_name,_email,_password))
			data = cursor.fetchall()
			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'User created successfully!'})
			else:
				return json.dumps({'error':str(data[0])})
			cursor.close()
			conn.close()
		else:
			return json.dumps({'html':'<span>All of the fields must be filled.</span>'})
	except Exception, e:
		return json.dumps({'error':str(e)})
		

if __name__ == "__main__":
	app.run(debug=True)