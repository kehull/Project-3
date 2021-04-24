import datetime as dt
import uuid
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.utils import to_categorical
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect)
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Customer = create_classes(db)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/predictions", methods=["GET", "POST"])
def send():
    offer_model = load_model("models/neural_network_model.h5")
    label_encoder=LabelEncoder()
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        age = request.form["age"]
        income=request.form["income"]
        label_encoder.fit(gender)
        encoded_gender=label_encoder.transform(gender)
        gender=to_categorical(encoded_gender)
        data=[gender,age,income]
        data_scaler=MinMaxScaler().fit(data)
        data_scaled = data_scaler.transform(data)
        encoded_predictions=offer_model.predict_classes(data_scaled)
        prediction_labels = label_encoder.inverse_transform(encoded_predictions)
        gender=label_encoder.inverse_transform(gender)
        customer_id=uuid.uuid4().hex
        date=dt.datetime.today().strftime('%Y%m%d')
        
        customer = Customer(name=name, customer_id=customer_id, gender=gender, age=age,income=income,offer=prediction_labels,membership_date=date)
        db.session.add(customer)
        db.session.commit()
        return redirect("/", code=302)
    return render_template("predictions.html")

if __name__ == "__main__":
    app.run()