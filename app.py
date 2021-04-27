import datetime as dt
import uuid
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect)

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') or "sqlite:///db.sqlite"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Customer = create_classes(db)
table_data=[]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/model", methods=["GET", "POST"])
def send():
    
    if request.method == "POST":
        table_data=table_data
        name = request.form["name"]
        gender = request.form["gender"]
        age = request.form["age"]
        income=request.form["income"]
        customer_id=uuid.uuid4().hex
        date=dt.datetime.today().strftime('%Y%m%d')
        offer=uuid.uuid4().hex
        customer = Customer(name=name, customer_id=customer_id, gender=gender, age=age,income=income,offer=offer,membership_date=date)
        db.session.add(customer)
        db.session.commit()
        test={"name":name,"customer_id":customer_id,"gender":gender,"age":age,"income":income,"offer":offer,"membership_date":date}
        table_data.append(test)
        
    return render_template("model.html",table_data=table_data)

if __name__ == "__main__":
    app.run()