from flask import Flask,request,render_template,make_response,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


sample = Flask(__name__)
sample.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///user.sqlite'
sample.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db= SQLAlchemy(sample)
ma= Marshmallow(sample)

class user(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(50))
    user_pass=db.Column(db.String(50))

    def __init__(self,user_name,user_pass):
        self.user_name=user_name
        self.user_pass=user_pass
    

class UserSchema(ma.Schema):
    class Meta:
        fields = ["user_name,user_pass"]

user_schema = UserSchema()
users_schema = UserSchema(many=True)



@sample.route("/")
def main():
    return render_template("index.html")

@sample.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name_input = request.form['username']
        user_pass_input = request.form['userpass']
 

    return render_template("login.html")

@sample.route("/reg", methods = ['GET','POST'])
def reg ():
    return render_template("register.html")

@sample.route("/registers", methods = ['GET','POST'])
def reg_user():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['userpass']
        new_user = user(user_name = username, user_pass=userpass)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
   
@sample.route("/alluser")
def users():
    all_users = user.query.all()
    return render_template('all_users.html',all_users=all_users)



if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)