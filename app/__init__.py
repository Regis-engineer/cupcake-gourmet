from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message = "Faça login para continuar."

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    login_manager.init_app(app)
    from .routes import main
    app.register_blueprint(main)
    with app.app_context():
        from .models import User, Category, Product
        db.create_all()
        if not User.query.filter_by(email="admin@cupcakelocal.test").first():
            admin = User(name="Administrador", email="admin@cupcakelocal.test", is_admin=True)
            admin.set_password("Admin123!")
            db.session.add(admin)
        if Category.query.count() == 0:
            cats = [Category(name="Clássicos"), Category(name="Especiais"), Category(name="Frutas")]
            db.session.add_all(cats)
            db.session.flush()
            db.session.add_all([
                Product(name="Chocolate Gourmet", description="Massa de chocolate com cobertura cremosa.", price=8.90, stock=30, category_id=cats[0].id),
                Product(name="Red Velvet", description="Massa red velvet com creme suave.", price=9.90, stock=25, category_id=cats[1].id),
                Product(name="Morango", description="Cupcake de baunilha com recheio de morango.", price=8.50, stock=20, category_id=cats[2].id),
                Product(name="Limão Siciliano", description="Massa leve com creme cítrico.", price=9.50, stock=15, category_id=cats[2].id),
            ])
        db.session.commit()
    return app
