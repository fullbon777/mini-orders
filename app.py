"""アプリケーション本体"""

import os
from flask import Flask, redirect, url_for, request, flash
from dotenv import load_dotenv
from models import db, Order, Product, Stock
from forms import OrderForm, RestockForm, ProductForm
from flask import render_template, request
from sqlalchemy import inspect


load_dotenv()
app = Flask(__name__, instance_relative_config=True)
app.secret_key = "dev-secret-key"
# 設計準拠: instance/app.db を使う
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///instance/app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/orders/new", methods=["GET", "POST"])
def new_order():
    form = OrderForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]

    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        if not product or not product.stock:
            flash("この商品には在庫データがありません。", "danger")
            return render_template("new_order.html", form=form)

        if product.stock.quantity < form.quantity.data:
            flash("在庫が足りません！", "danger")
            return render_template("new_order.html", form=form)

        # 在庫を減らす
        product.stock.quantity -= form.quantity.data

        order = Order(
            customer_name=form.customer_name.data,
            product_id=form.product_id.data,  # ← こっちにする
            quantity=form.quantity.data,
            desired_date=form.desired_date.data,
            note=form.note.data,
        )

        db.session.add(order)
        db.session.commit()
        flash("Order created successfully!", "success")
        return redirect(url_for("orders"))
    return render_template("new_order.html", form=form, products=Product.query.all())


@app.route("/orders")
def orders():

    customer = request.args.get("customer")
    item = request.args.get("item")
    query = Order.query
    if customer:
        query = query.filter(Order.customer_name.contains(customer))
    if item:
        query = query.join(Order.product).filter(Product.name.contains(item))

    page = request.args.get("page", 1, type=int)
    per_page = 10
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template(
        "orders.html", orders=pagination.items, pagination=pagination
    )


@app.route("/orders/<int:order_id>/edit", methods=["GET", "POST"])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    form = OrderForm(obj=order)

    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]

    if form.validate_on_submit():
        old_quantity = order.quantity
        new_quantity = form.quantity.data
        diff = new_quantity - old_quantity
        if order.product and order.product.stock:
            if diff > 0 and order.product.stock.quantity < diff:
                flash("在庫が足りません！", "danger")
                return render_template("edit_order.html", form=form, order=order)
            order.product.stock.quantity -= diff

        form.populate_obj(order)
        db.session.commit()
        flash("Order updated!", "success")
        return redirect(url_for("orders"))
    return render_template("edit_order.html", form=form, order=order)


@app.route("/orders/<int:order_id>/delete", methods=["POST"])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)

    if order.product and order.product.stock:
        order.product.stock.quantity += order.quantity

    db.session.delete(order)
    db.session.commit()
    flash("Order deleted!", "success")
    return redirect(url_for("orders"))


@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("order_detail.html", order=order)


@app.route("/products", methods=["GET", "POST"])
def products():
    items = Product.query.all()
    # form = RestockForm()

    if request.method == "POST":
        product_id = request.form.get("product_id")
        amount = request.form.get("amount")

        if product_id and amount:
            product = Product.query.get(int(product_id))
            if product and product.stock:
                product.stock.quantity += int(amount)
                db.session.commit()
                flash(f"{product.name} の在庫を {amount} 個補充しました！", "success")
            else:
                flash("在庫データが見つかりません。", "danger")
        return redirect(url_for("products"))

    return render_template("products.html", items=items)


@app.route("/products/new", methods=["GET", "POST"])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        # 既存商品チェック
        existing = Product.query.filter_by(name=form.name.data).first()
        if existing:
            flash("同じ名前の商品がすでに存在します。", "danger")
            return redirect(url_for("products"))
        filename = f"images/{form.name.data.lower()}.jpg"
        product = Product(
            name=form.name.data, price=form.price.data, image_url=filename
        )
        stock = Stock(product=product, quantity=0)  # 初期在庫はゼロ
        db.session.add_all([product, stock])
        db.session.commit()
        flash(f"{product.name} を追加しました！", "success")
        return redirect(url_for("products"))

    return render_template("new_product.html", form=form)


if __name__ == "__main__":
    with app.app_context():
        # ① テーブルを必ず先に作る
        db.create_all()
        # ② テーブル一覧を確認
        inspector = inspect(db.engine)
        print(">>> tables:", inspector.get_table_names())

        # ② その後に初期データ投入
        if Product.query.count() == 0:
            apple = Product(name="Apple", price=100, image_url="images/apple.jpg")
            orange = Product(name="Orange", price=80, image_url="images/orange.jpg")

            stock1 = Stock(product=apple, quantity=10)
            stock2 = Stock(product=orange, quantity=5)

            db.session.add_all([apple, orange, stock1, stock2])
            db.session.commit()
            print("初期データ投入しました！")

        # ③ デバッグ出力
        print("=== Products ===")
        for p in Product.query.all():
            print(p.id, p.name, p.price, p.stock)
        print("=== Stocks ===")
        for s in Stock.query.all():
            print(s.id, s.product_id, s.quantity)
        print("=== Products after order ===")
        for p in Product.query.all():
            print(p.id, p.name, p.price, p.stock.quantity if p.stock else None)

    # ④ 最後にサーバ起動
    app.run(debug=True)
