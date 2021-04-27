import datetime as dt
import uuid
from models import create_classes
import os
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect)
import joblib
from sklearn.linear_model import LogisticRegression


app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['JSON_SORT_KEYS'] = False
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
    global table_data
    table_data=table_data
    #create var to store table data
    
   
    
    #load in model
    model=joblib.load('models/random_forest_model.h5')   
    
    #postgres form setup and table vars
    if request.method == "POST":
        #get info from forms
        name = request.form["name"]
        gender = request.form["gender"]
        age = request.form["age"]
        income=request.form["income"]
        
        #create customer id
        customer_id=uuid.uuid4().hex
        
        #create date
        date=dt.datetime.today().strftime('%Y%m%d')
        
      
        #store data into model data
        model_data=[[age,income]]
        
        #predict
        predictions_array = model.predict(model_data)
        prediction=predictions_array[0]
        
        #create offer for db
        offer=""
        
        # create giant if statement to determine prediction string
        if prediction == 0:
            offer='9b98b8c7a33c4b65b9aebfe6a799e6d9'
        elif prediction == 1:
            offer = 'ae264e3637204a6fb9bb56bc8210ddfd'
        elif prediction == 2:
            offer = 'f19421c1d4aa40978ebb69ca19b0e20d'
        elif prediction == 3:
            offer = 'fafdcd668e3743c1bb461111dcafc2a4'
        elif prediction == 4:
            offer = '2906b810c7d4411798c6938adc9daaa5'
        elif prediction == 5:
            offer = '4d5c57ea9a6940dd891ad53e9dbe8da0'
        elif prediction == 6:
            offer = '2298d6c36e964ae4a3e7e9706d1fb8c2'
        else:
            offer= '0b1e1539f2cc45b7b9fa7c272da2e1d7'

        #store data to db
        customer = Customer(name=name, customer_id=customer_id, gender=gender, age=age,income=income,offer=offer,membership_date=date)
        db.session.add(customer)
        db.session.commit()
        #create dictionary to append to test data for table
        test={"name":name,"customer_id":customer_id,"gender":gender,"age":age,"income":income,"offer":offer,"membership_date":date}
        #append to table data
        table_data.append(test)
        table_data=table_data
         
        
    return render_template("model.html",table_data=table_data)

@app.route('/model/api')
def customer():
    results = db.session.query(Customer.name, Customer.customer_id, Customer.gender,Customer.age,Customer.income,Customer.offer,Customer.membership_date).all()
    customer_data = {"customer_data":[]}
    for name,customer_id,gender,age,income,offer,membership_date in results:

        test_data = {
            "name": name,
            "customer_id": customer_id,
            "gender": gender,
            "age": age,
            "income": income,
            "offer": offer,
            "membership_date": membership_date
        }
        customer_data["customer_data"].append(test_data)
    return jsonify(customer_data)

@app.route('/interviews/benfierce')
def ben():
    return render_template("ben.html")

@app.route('/interviews/jenkaslowon')
    def jen():
        return render_template("jen.html")

@app.route('/disclaimer')
def disclaimer():
    return render_template("disclaimer.html")

@app.route('/casestudy/delmar')
    def delmar():
        return render_template("delmar.html")

@app.route('/casestudy/showme')
def showme():
    return render_template('showme.html')

if __name__ == "__main__":
    app.run()