def create_classes(db):
    class Customer(db.Model):
        __tablename__ = 'customer'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64))
        customer_id=db.Column(db.VARCHAR)
        gender=db.Column(db.String)
        age=db.Column(db.Integer)
        income=db.column(db.Float)
        offer=db.column(db.VARCHAR)
        membership_date=db.column(db.VARCHAR)


        def __repr__(self):
            return '<Customer %r>' % (self.name)
    return Customer