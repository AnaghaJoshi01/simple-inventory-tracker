import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load database URL from .env file
load_dotenv()

app = Flask(__name__)

# Connect to Neon Console Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Item Model based on your DBMS report
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=0)

# Main Page Route
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

# Add Item Route
@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    category = request.form.get('category')
    quantity = request.form.get('quantity')
    
    new_item = Item(name=name, category=category, quantity=int(quantity))
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Automatically creates the 'items' table in Neon
    app.run(host='0.0.0.0', port=5000)
