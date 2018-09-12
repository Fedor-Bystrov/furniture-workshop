from datetime import datetime
from decimal import Decimal

from workshop.model import Cart, Customer, CustomerLocale, Purchase


def create_cart(request_body: dict) -> Cart:
    first_name = request_body.get('firstName')
    last_name = request_body.get('lastName')
    middle_name = request_body.get('middleName')
    email = request_body.get('email')
    phone = request_body.get('phone')
    shipping_address = request_body.get('shippingAddress')
    purchases_data = request_body.get('purchases')
    price = request_body.get('price')
    description = request_body.get('description')

    customer = Customer(first_name=first_name,
                        last_name=last_name,
                        middle_name=middle_name,
                        locale=CustomerLocale.RU,
                        email=email,
                        phone=phone)

    purchases = [Purchase(product_id=data.get('productId'), quantity=data.get('quantity'))
                 for data in purchases_data]

    cart = Cart(customer=customer,
                purchases=purchases,
                price=price,
                shipping_address=shipping_address,
                description=description)

    return cart


def update_cart(cart: Cart, request_body: dict) -> None:
    first_name = request_body.get('firstName')
    if first_name:
        cart.customer.first_name = first_name

    last_name = request_body.get('lastName')
    if last_name:
        cart.customer.last_name = last_name

    middle_name = request_body.get('middleName')
    if middle_name:
        cart.customer.middle_name = middle_name

    email = request_body.get('email')
    if email:
        cart.customer.email = email

    phone = request_body.get('phone')
    if phone:
        cart.customer.phone = phone

    shipping_address = request_body.get('shippingAddress')
    if shipping_address:
        cart.shipping_address = shipping_address

    purchases = request_body.get('purchases')
    if purchases:
        update_purchases(cart, purchases)
    else:
        cart.purchases = None

    price = request_body.get('price')
    if price:
        cart.price = Decimal(price)

    description = request_body.get('description')
    if description:
        cart.description = description


def update_purchases(cart: Cart, data: dict) -> None:
    for purchase in data:

        product_id = purchase.get('productId')
        quantity = purchase.get('quantity')

        if product_id and quantity:

            purchase_to_update = get_purchase_with_product_id(cart, product_id)

            if purchase_to_update:
                purchase_to_update.quantity = quantity
            else:
                cart.purchases.append(Purchase(creation_time=datetime.now(),
                                               cart_id=cart.cart_id,
                                               product_id=product_id,
                                               quantity=quantity))
        else:
            # TODO причесать эксепшн
            raise RuntimeError("product or price is absent")


def get_purchase_with_product_id(cart: Cart, product_id: int) -> Purchase:
    purchases = list(filter(lambda p, p_id=product_id: p.product_id == p_id, cart.purchases))
    return purchases[0] if len(purchases) > 0 else None
