import os
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
        admin_email = os.getenv("ADMIN_EMAIL", "").strip().lower()
        admin_password = os.getenv("ADMIN_PASSWORD", "")

        if bool(admin_email) != bool(admin_password):
            raise RuntimeError(
                "Configure ADMIN_EMAIL e ADMIN_PASSWORD juntos."
            )

        if admin_email and admin_password:
            admin = User.query.filter_by(email=admin_email).first()

            if admin is None:
                admin = User(
                    name=os.getenv("ADMIN_NAME", "Administrador"),
                    email=admin_email,
                    is_admin=True
                )
                admin.set_password(admin_password)
                db.session.add(admin)
            elif not admin.is_admin:
                raise RuntimeError(
                    "ADMIN_EMAIL já pertence a uma conta não administrativa."
                )
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
