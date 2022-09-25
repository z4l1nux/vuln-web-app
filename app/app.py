
from flask import Flask, request, redirect, url_for, session,render_template,escape
from flask_mysqldb import MySQL
import mysql.connector




app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'key'


@app.route('/pythonlogin/test')
def test():
    return render_template('index.html')


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
   
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       
        username = request.form['username']
        password = request.form['password']
       

        config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'knights'
        }

        mydb = mysql.connector.connect(**config)

        mycursor = mydb.cursor()

        # mycursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        

        # mycursor.execute("SELECT * FROM knights.accounts WHERE username ='' or 1=1--' and password ='' or 1=1--'" )
        mycursor.execute("SELECT * FROM knights.accounts WHERE username ='" +username +"' and password ='"+ password +"'" )

        
        account = mycursor.fetchone()
       
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # return 'Logged in successfully!'
            return("""<h2> passed! 😎</h2> """
          """<br>
          <p>Welcome back,"""+ session['username']+"""!</p>
          <div class="links">
				<a href='"""+url_for('logout')+"""'">Logout</a>
			</div>""")
        else:
            msg = 'Incorrect username/password!'
    return (
        	"""<h2> LOGIN 🦊  </h2>"""
		"""<br>"""
		"""
			<form action='"""+url_for('login')+"""' method="post">
				<label for="username">
					<i class="fas fa-user"></i>
				</label>
				<input type="text" name="username" placeholder="Username" id="username" required>
				<label for="password">
					<i class="fas fa-lock"></i>
				</label>
				<input type="password" name="password" placeholder="Password" id="password" required>
				
				<input type="submit" value="Login">

                <div class="msg">"""+ msg+"""</div>
			</form>
		"""

    )


@app.route('/pythonlogin/logout')
def logout():
   
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   
   return redirect(url_for('login'))

@app.route("/")
def index():
    
    celsius = request.args.get("celsius", "")


    if celsius:
            fahrenheit = fahrenheit_from(celsius)
    else:
            fahrenheit = ""


    # try:
    #     if celsius:
    #         fahrenheit = fahrenheit_from(celsius)
    #     else:
    #         fahrenheit = ""
    # except ValueError:
    #     return "invalid input"

    return (
        	"""<h2> It's a simple web app! 🦊 </h2>"""
		"""<br>"""
		"""<form action="" method="get">
                <input type="text" name="celsius">
                <input type="submit" value="Convert">
            </form>"""
        + "Fahrenheit: "
        + '<a id="fahrenheit">' +fahrenheit+ '</a>'

    )
 
@app.route("/<int:celsius>")
def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    fahrenheit = float(celsius) * 9 / 5 + 32
    fahrenheit = round(fahrenheit, 3) 
    return str(fahrenheit)

@app.route("/<string:script>")
def run(script):
    script=request.args.get("script", "")

    # script = str(escape(request.args.get("script", "")))


    return (
	"""<h2> Run! 🕸 </h2>"""
	"""<form action="" method="get">
                <input type="text" name="script">
                <input type="submit" value="Run">
            </form>"""
    + '<a id="script">' + script + '</a>'
    )

# @app.after_request
# def add_security_headers(resp):
#     resp.headers['Content-Security-Policy']='default-src \'self\''
#     return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True)
    # app.run(host='0.0.0.0',debug = True)
