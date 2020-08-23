from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dkyman420@localhost/form_test'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dcdmycnfftcczr:640e7d16629b5d6e7283b557a3b495f82ad98fb4dabbc56c6d8c1107238618d0@ec2-52-86-116-94.compute-1.amazonaws.com:5432/drgnc5ed6vhf'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    employee = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, employee, rating, comments):
        self.customer = customer
        self.employee = employee
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        employee = request.form['employee']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(f"{customer}, {employee}, {rating}, {comments}")
        if customer == "" or employee == "":
            return render_template('index.html', message="Please Enter Required Field!")
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, employee, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, employee, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message="You have already submitted your feedback, Thank you!")


if __name__ == '__main__':
    app.run()
