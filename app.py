import datetime as dt
import uuid
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect)
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') or "sqlite:///db.sqlite"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Customer = create_classes(db)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/model", methods=["GET", "POST"])
def send():
    #create var to store table data
    table_data=[]
    #def label encoder
    label_encoder=LabelEncoder()
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
        
        #encode gender for model
        label_encoder.fit(gender)
        encoded_gender=label_encoder.transform(gender)
        
        #encode customer_id for model
        label_encoder.fit(customer_id)
        encoded_id=label_encoder.transform(customer_id)
        
        #store data into model data
        model_data=[[encoded_id,encoded_gender,age,income]]
        
        #predict
        predictions_array = model.predict(model_data)
        prediction=predictions_array[0]
        
        #create offer for db
        offer=""
        
        # create giant if statement to determine prediction string
        if prediction = 0:
            offer='9b98b8c7a33c4b65b9aebfe6a799e6d9'
        elif prediction=1:
            offer = 'ae264e3637204a6fb9bb56bc8210ddfd'
        elif prediction=2:
            offer = 'f19421c1d4aa40978ebb69ca19b0e20d'
        elif prediction=3:
            offer = 'fafdcd668e3743c1bb461111dcafc2a4'
        elif prediction=4:
            offer = '2906b810c7d4411798c6938adc9daaa5'
        elif prediction=5:
            offer = '4d5c57ea9a6940dd891ad53e9dbe8da0'
        elif prediction=6:
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
        
    return render_template("model.html",table_data=table_data)

if __name__ == "__main__":
    app.run()