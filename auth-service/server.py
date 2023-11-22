import jwt,datetime,os
from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from envvar import setVar
import uuid

server = Flask(__name__)
mysql = MySQL(server)
#mysql.connection.autocommit = True
setVar()

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = 3306



@server.route("/login",methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "MISSING CREDENTIALS",401
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT username,password FROM trx_users where username=%s",(auth.username,)
    )
    if res>0:
        user = cur.fetchone()
        email = user[0]
        password = user[1]
        if auth.username!=email and auth.password!=password:
            return "INVALID CREDENTIALS",401
        else:
            return createJWT(email,os.environ.get("JWT_SECRET"),True) 
    else:
        return "INVALID CREDENTIALS",401
        

def createJWT(username,secret,status):
    print(username,secret,status)
    return jwt.encode(
        {
            "username": username,
            "exp":datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin":status,
        },
        secret,algorithm='HS256'
    )

@server.route("/validate",methods=["GET"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "MISSING CREDENTIALS",401
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt,os.environ.get("JWT_SECRET"),algorithms=['HS256']
        )
    except:
        return "UNAUTHORIZED",403
    return decoded,200

@server.route("/signup",methods=["POST"])
def signUp():
    email = request.form["username"]
    password  = request.form["password"]
    firstName = request.form["firstname"]
    lastName = request.form["lastname"]
    print(email,password,firstName,lastName)
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO trx_users(user_id,username,password,first_name,last_name,status,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s)",(str(uuid.uuid4()),email,password,firstName,lastName,1,datetime.datetime.now(tz=datetime.timezone.utc))
    )
    mysql.connection.commit()
    return createJWT(email,os.environ.get("JWT_SECRET"),True) 

@server.route("/",methods=["GET"])
def welcome():
    return jsonify({
        "status": True,
        "message": "success",
        "desc":"Welcome to our Microservices Architecture"
    })


if __name__ == "__main__":
    #server.run(host="0.0.0.0",port=5000)
    server.run(debug=False)

