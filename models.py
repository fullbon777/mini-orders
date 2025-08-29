"""DBモデル定義"""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

# from app import db

db = SQLAlchemy()

STATUS_CHOICES = ("received", "preparing", "shipped")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product", back_populates="orders")
    quantity = db.Column(db.Integer, nullable=False, default=1)
    desired_date = db.Column(db.Date)  # type: date | None
    status = db.Column(db.String(20), nullable=False, default="received")  # 設計準拠
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_orders_quantity_nonneg"),
    )

    def set_status(self, value: str):
        if value not in STATUS_CHOICES:
            raise ValueError(f"status must be one of {STATUS_CHOICES}")
        self.status = value


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255))
    stock = db.relationship("Stock", back_populates="product", uselist=False)
    orders = db.relationship("Order", back_populates="product")


class Stock(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, unique=True
    )
    product = db.relationship("Product", back_populates="stock")
