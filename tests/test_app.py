import pytest
from app import create_app, db
from app.models import User, Category, Product, Order, Payment

@pytest.fixture
def app():
    app=create_app({"TESTING":True,"SQLALCHEMY_DATABASE_URI":"sqlite:///:memory:","SECRET_KEY":"test"})
    with app.app_context():
        db.drop_all(); db.create_all()
        cat=Category(name="Teste"); db.session.add(cat); db.session.flush()
        db.session.add(Product(name="Cupcake Teste",description="Produto de teste",price=10,stock=3,category_id=cat.id))
        u=User(name="Cliente Teste",email="cliente@example.com"); u.set_password("123456"); db.session.add(u)
        admin=User(name="Admin",email="admin@example.com",is_admin=True); admin.set_password("Admin123!"); db.session.add(admin); db.session.commit()
    return app

def login(client,email,password):
    return client.post('/login',data={'email':email,'password':password},follow_redirects=True)

def test_home(app):
    r=app.test_client().get('/'); assert r.status_code==200; assert b'Cupcake Gourmet' in r.data

def test_catalog(app):
    r=app.test_client().get('/catalogo'); assert r.status_code==200; assert b'Cupcake Teste' in r.data

def test_register_validation(app):
    r=app.test_client().post('/cadastro',data={'name':'A','email':'x','password':'1'},follow_redirects=True); assert b'Preencha nome' in r.data

def test_add_cart_stock_limit(app):
    c=app.test_client(); r=c.post('/carrinho/adicionar/1',follow_redirects=True); assert r.status_code==200; assert b'Cupcake Teste' in r.data
    with c.session_transaction() as sess: assert sess['cart']['1']==1
    for _ in range(2): c.post('/carrinho/adicionar/1')
    c.post('/carrinho/adicionar/1',follow_redirects=True)
    with c.session_transaction() as sess: assert sess['cart']['1']==3

def test_checkout_creates_order_and_payment(app):
    c=app.test_client(); login(c,'cliente@example.com','123456'); c.post('/carrinho/adicionar/1')
    r=c.post('/checkout',data={'street':'Rua Teste','number':'10','city':'Brasilia','state':'DF','zip_code':'70000-000','payment':'PIX'},follow_redirects=True)
    assert r.status_code==200; assert b'Pedido criado' in r.data
    with app.app_context():
        o=Order.query.one(); assert o.total == 10; assert o.status=='Recebido'; assert Payment.query.one().method=='PIX'; assert Product.query.get(1).stock==2

def test_admin_can_edit_product(app):
    c=app.test_client(); login(c,'admin@example.com','Admin123!')
    r=c.post('/admin/produto/1/editar',data={'name':'Cupcake Atualizado','description':'Nova descricao','price':'12.50','stock':'8','category_id':'1'},follow_redirects=True)
    assert r.status_code==200; assert b'Produto atualizado' in r.data
    with app.app_context(): assert Product.query.get(1).name=='Cupcake Atualizado'; assert Product.query.get(1).stock==8

def test_non_admin_forbidden(app):
    c=app.test_client(); login(c,'cliente@example.com','123456'); assert c.get('/admin').status_code==403
