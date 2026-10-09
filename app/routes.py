from decimal import Decimal, InvalidOperation
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from . import db
from .models import User, Category, Product, Address, Order, OrderItem, Payment
from .services import calculate_cart, can_add

main=Blueprint("main",__name__)

@main.route("/health")
def health():
    return {"status": "ok", "service": "cupcake-gourmet"}, 200
STATUSES=["Recebido","Confirmado","Em preparação","Pronto para entrega","Saiu para entrega","Entregue","Cancelado"]

def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin: abort(403)

def cart_context():
    items,total=calculate_cart(session.get("cart",{})); return items,total

@main.context_processor
def inject():
    items,total=cart_context(); return {"cart_count":sum(q for _,q,_ in items),"cart_total":total}

@main.route("/")
def home():
    products=Product.query.filter_by(active=True).order_by(Product.id.desc()).limit(6).all()
    return render_template("home.html",products=products)

@main.route("/catalogo")
def catalog():
    q=request.args.get("q","").strip(); category=request.args.get("category","")
    query=Product.query.filter_by(active=True)
    if q: query=query.filter(or_(Product.name.ilike(f"%{q}%"),Product.description.ilike(f"%{q}%")))
    if category.isdigit(): query=query.filter_by(category_id=int(category))
    return render_template("catalog.html",products=query.order_by(Product.name).all(),categories=Category.query.filter_by(active=True).all(),q=q,category=category)

@main.route("/produto/<int:pid>")
def product(pid): return render_template("product.html",product=db.get_or_404(Product,pid))

@main.route("/cadastro",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").strip().lower(); password=request.form.get("password","")
        if len(name)<3 or "@" not in email or len(password)<6: flash("Preencha nome, e-mail válido e senha com pelo menos 6 caracteres.","error"); return redirect(url_for("main.register"))
        if User.query.filter_by(email=email).first(): flash("E-mail já cadastrado.","error"); return redirect(url_for("main.register"))
        u=User(name=name,email=email); u.set_password(password); db.session.add(u); db.session.commit(); login_user(u); flash("Cadastro realizado com sucesso!","success"); return redirect(url_for("main.home"))
    return render_template("register.html")

@main.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=User.query.filter_by(email=request.form.get("email","").strip().lower()).first()
        if u and u.check_password(request.form.get("password","")): login_user(u); return redirect(url_for("main.admin") if u.is_admin else url_for("main.home"))
        flash("E-mail ou senha inválidos.","error")
    return render_template("login.html")

@main.route("/logout")
@login_required
def logout(): logout_user(); return redirect(url_for("main.home"))

@main.route("/carrinho")
def cart():
    items,total=cart_context(); return render_template("cart.html",items=items,total=total)

@main.route("/carrinho/adicionar/<int:pid>",methods=["POST"])
def add_cart(pid):
    p=db.get_or_404(Product,pid)
    if not p.active:
        abort(404)
    cart=session.setdefault("cart",{}); qty=int(cart.get(str(pid),0))+1
    if not can_add(p,qty): flash("Quantidade indisponível em estoque.","error")
    else: cart[str(pid)]=qty; session.modified=True; flash(f"{p.name} adicionado ao carrinho.","success")
    return redirect(request.referrer or url_for("main.catalog"))

@main.route("/carrinho/atualizar",methods=["POST"])
def update_cart():
    cart=session.setdefault("cart",{})
    for key,val in request.form.items():
        if not key.startswith("qty_"): continue
        pid=key[4:]
        try: qty=int(val)
        except ValueError: continue
        p=db.session.get(Product,int(pid))
        if p and 0<=qty<=p.stock:
            if qty==0: cart.pop(pid,None)
            else: cart[pid]=qty
    session.modified=True; flash("Carrinho atualizado.","success"); return redirect(url_for("main.cart"))

@main.route("/carrinho/remover/<int:pid>",methods=["POST"])
def remove_cart(pid): session.setdefault("cart",{}).pop(str(pid),None); session.modified=True; return redirect(url_for("main.cart"))

@main.route("/checkout",methods=["GET","POST"])
@login_required
def checkout():
    items,total=cart_context()
    if not items: return redirect(url_for("main.catalog"))
    if request.method=="POST":
        required=["street","number","city","state","zip_code","payment"]
        if any(not request.form.get(x,"").strip() for x in required): flash("Preencha todos os campos obrigatórios.","error"); return render_template("checkout.html",items=items,total=total)
        for p,q,_ in items:
            if not p.active: flash(f"O produto {p.name} não está mais disponível.","error"); return redirect(url_for("main.cart"))
            if p.stock<q: flash(f"Estoque insuficiente para {p.name}.","error"); return redirect(url_for("main.cart"))
        a=Address(user_id=current_user.id,street=request.form["street"].strip(),number=request.form["number"].strip(),city=request.form["city"].strip(),state=request.form["state"].strip().upper(),zip_code=request.form["zip_code"].strip())
        o=Order(user_id=current_user.id,address=a,total=total,status="Recebido"); db.session.add(o); db.session.flush()
        for p,q,_ in items: db.session.add(OrderItem(order_id=o.id,product_id=p.id,quantity=q,unit_price=p.price)); p.stock-=q
        payment=Payment(order_id=o.id,method=request.form["payment"],status="Simulado",transaction_code=f"SIM-{uuid4().hex[:10].upper()}"); db.session.add(payment)
        db.session.commit(); session["cart"]={}; flash("Pedido criado com sucesso! Pagamento registrado em modo simulado.","success"); return redirect(url_for("main.order_detail",oid=o.id))
    return render_template("checkout.html",items=items,total=total)

@main.route("/pedidos")
@login_required
def orders(): return render_template("orders.html",orders=Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all())

@main.route("/pedido/<int:oid>")
@login_required
def order_detail(oid):
    o=db.get_or_404(Order,oid)
    if o.user_id!=current_user.id and not current_user.is_admin: abort(403)
    return render_template("order.html",order=o,statuses=STATUSES)

@main.route("/admin")
@login_required
def admin():
    admin_required(); products=Product.query.order_by(Product.active.desc(),Product.name).all(); orders=Order.query.order_by(Order.created_at.desc()).all(); categories=Category.query.order_by(Category.name).all()
    metrics={"products":Product.query.filter_by(active=True).count(),"low_stock":Product.query.filter(Product.active==True,Product.stock<=5).count(),"orders":Order.query.count(),"users":User.query.filter_by(is_admin=False).count()}
    return render_template("admin.html",products=products,orders=orders,categories=categories,metrics=metrics,statuses=STATUSES)

@main.route("/admin/produto",methods=["POST"])
@login_required
def admin_product():
    admin_required()
    try: price=Decimal(request.form.get("price","0")); stock=int(request.form.get("stock","0")); category_id=int(request.form.get("category_id","0"))
    except (InvalidOperation,ValueError): flash("Preço, estoque ou categoria inválidos.","error"); return redirect(url_for("main.admin"))
    name=request.form.get("name","").strip()
    if not name or price<0 or stock<0 or not db.session.get(Category,category_id): flash("Revise os dados do produto.","error"); return redirect(url_for("main.admin"))
    p=Product(name=name,description=request.form.get("description","").strip(),price=price,stock=stock,category_id=category_id,image_url=request.form.get("image_url","").strip())
    db.session.add(p); db.session.commit(); flash("Produto cadastrado.","success"); return redirect(url_for("main.admin"))

@main.route("/admin/produto/<int:pid>/editar",methods=["POST"])
@login_required
def admin_edit_product(pid):
    admin_required(); p=db.get_or_404(Product,pid)
    try: p.price=Decimal(request.form.get("price","0")); p.stock=int(request.form.get("stock","0")); p.category_id=int(request.form.get("category_id","0"))
    except (InvalidOperation,ValueError): flash("Dados inválidos.","error"); return redirect(url_for("main.admin"))
    p.name=request.form.get("name","").strip(); p.description=request.form.get("description","").strip(); p.image_url=request.form.get("image_url","").strip(); db.session.commit(); flash("Produto atualizado.","success"); return redirect(url_for("main.admin"))

@main.route("/admin/produto/<int:pid>/alternar",methods=["POST"])
@login_required
def toggle_product(pid):
    admin_required(); p=db.get_or_404(Product,pid); p.active=not p.active; db.session.commit(); flash("Status do produto atualizado.","success"); return redirect(url_for("main.admin"))

@main.route("/admin/categoria",methods=["POST"])
@login_required
def admin_category():
    admin_required(); name=request.form.get("name","").strip()
    if not name: flash("Informe o nome da categoria.","error")
    elif Category.query.filter_by(name=name).first(): flash("Categoria já cadastrada.","error")
    else: db.session.add(Category(name=name)); db.session.commit(); flash("Categoria cadastrada.","success")
    return redirect(url_for("main.admin"))

@main.route("/admin/pedido/<int:oid>",methods=["POST"])
@login_required
def admin_order(oid):
    admin_required(); o=db.get_or_404(Order,oid); status=request.form.get("status")
    if status not in STATUSES: flash("Status inválido.","error")
    else: o.status=status; db.session.commit(); flash("Status do pedido atualizado.","success")
    return redirect(url_for("main.admin"))
