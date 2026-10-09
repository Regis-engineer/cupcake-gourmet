from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "app_user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    addresses = db.relationship("Address", backref="user", lazy=True, cascade="all, delete-orphan")
    orders = db.relationship("Order", backref="user", lazy=True)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id): return db.session.get(User, int(user_id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    products = db.relationship("Product", backref="category", lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    image_url = db.Column(db.String(300), default="")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    street = db.Column(db.String(160), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(12), nullable=False)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"), nullable=True)
    status = db.Column(db.String(40), default="Recebido", nullable=False)
    total = db.Column(db.Numeric(10,2), default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    address = db.relationship("Address")
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")
    payment = db.relationship("Payment", backref="order", uselist=False, cascade="all, delete-orphan")

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10,2), nullable=False)
    product = db.relationship("Product")

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, unique=True)
    method = db.Column(db.String(40), nullable=False)
    status = db.Column(db.String(40), default="Simulado", nullable=False)
    transaction_code = db.Column(db.String(80), nullable=False)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
