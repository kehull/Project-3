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
from sklearn.ensemble import RandomForestClassifier
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
    table_data=[]
    label_encoder=LabelEncoder()
    model=joblib.load("models/random_forest_model.h5")   
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        age = request.form["age"]
        income=request.form["income"]
        customer_id=uuid.uuid4().hex
        date=dt.datetime.today().strftime('%Y%m%d')
        gender_encode=label_encoder.fit(gender)
        encoded_gender=label_encoder.transform(gender_encode)
        id_encode=label_encoder.fit(customer_id)
        encoded_id=label_encoder.transform(id_encode)
        model_data=[encoded_id,encoded_gender,age,income]
        encoded_predictions = model.predict_classes(model_data)
        prediction_labels = label_encoder.inverse_transform(encoded_predictions)
        offer=prediction_labels
        customer = Customer(name=name, customer_id=customer_id, gender=gender, age=age,income=income,offer=offer,membership_date=date)
        db.session.add(customer)
        db.session.commit()
        test={"name":name,"customer_id":customer_id,"gender":gender,"age":age,"income":income,"offer":offer,"membership_date":date}
        table_data.append(test)
        
    return render_template("model.html",table_data=table_data)

if __name__ == "__main__":
    app.run()