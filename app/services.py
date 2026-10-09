from decimal import Decimal
from . import db
from .models import Product

def calculate_cart(cart):
    items=[]; total=Decimal("0")
    for pid, qty in cart.items():
        product=db.session.get(Product,int(pid))
        qty=int(qty)
        if product and product.active and qty>0:
            subtotal=product.price*qty
            items.append((product,qty,subtotal)); total += subtotal
    return items,total

def can_add(product, quantity):
    return product.active and product.stock >= quantity and quantity > 0
