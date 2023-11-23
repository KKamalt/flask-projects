# from itertools import product
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ecommerce.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.Column(db.String(200),nullable=False)

with app.app_context():
    db.create_all()



cart_ = []  # Simulate a shopping cart as a list

@app.route('/')
def index():
    products = Product.query.all()
    for product in products:
        print(f"{product.product}")
    return render_template('index.html', products=products)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product:
        cart_.append(product)
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart_)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
