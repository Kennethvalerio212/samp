from flask import Flask,request,render_template,make_response,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


sample = Flask(__name__)
sample.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///user.sqlite'
sample.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db= SQLAlchemy(sample)
ma= Marshmallow(sample)

class Heart(db.Model):
    __tablename__="heart"
    heart_id=db.Column(db.Integer,primary_key=True)
    heart_date=db.Column(db.String(50))
    heart_rate=db.Column(db.String(50))

    def __init__(self,heart_id,heart_date,heart_rate):
        self.heart_id=heart_id
        self.heart_date=heart_date
        self.heart_rate =heart_rate
    

class HeartSchema(ma.Schema):
    class Meta:
        fields=["heart_id","heart_date","heart_rate"]

heart_schema=HeartSchema()
hearts_schema=HeartSchema(many=True)



@sample.route("/")
def main():
    return render_template("index.html")

@sample.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@sample.route("/reg", methods = ['GET','POST'])
def reg ():
    return render_template("register.html")

@sample.route("/registers", methods = ['POST'])
def reg_user():
    if request.method == 'POST':
        heart_id = request.form['heart_id']
        heart_rate = request.form['heart_rate']
        heart_date= request.form['heart_date']
        new_heart = Heart(heart_id = heart_id,heart_date =heart_date, heart_rate=heart_rate)
        db.session.add(new_heart)
        db.session.commit()
        return heart_schema.jsonify(new_heart)
   
@sample.route("/allhearts")
def users():
    result = Heart.query.all()
    #return hearts_schema.jsonify(result).data
    return render_template("all_users.html",result=result)

@sample.route('/hearts/<heart_id>',methods=['GET'])
def read_heart(heart_id):
    heart=Heart.query.get(heart_id)
    result= heart_schema.dump(heart)
    return heart_schema.jsonify(result)

@sample.route("/update", methods=['GET', 'POST'])
def update():
    return render_template("update.html")

@sample.route('/hearts/<heart_id>',methods=['PUT'])

def update_heart(heart_id):
    heart=Heart.query.get(heart_id)

    heart_rate=request.json.get('heart_rate')
    heart_date=request.json.get('heart_date')

    heart.heart_date= heart_date
    heart.heart_rate=heart_rate
    db.session.commit()

    return heart_schema.jsonify(heart)

@sample.route('/hearts/<heart_id>',methods=['DELETE'])
def delete_heart(heart_id):
    heart=Heart.query.get(heart_id)
    db.session.delete(heart)
    db.session.commit()
    
    return heart_schema.jsonify(heart)


if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)