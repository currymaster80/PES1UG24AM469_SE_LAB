
"""E-commerce shopping cart and checkout management system."""

import hashlib
import secrets


CART_ITEMS = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}


def add_item_to_cart(item_id, name, price, qty=1, audit_log=None):
    """Add a new item to the cart and optionally record the operation."""
    if item_id in CART_ITEMS:
        return False

    if price < 0 or qty < 1:
        raise ValueError("Price must be non-negative and quantity positive.")

    if audit_log is None:
        audit_log = []

    CART_ITEMS[item_id] = {"name": name, "price": price, "qty": qty}
    audit_log.append(f"Added {item_id} with price {price:.2f}")
    return True


def remove_item_from_cart(item_id):
    """Remove an item from the cart, returning whether it existed."""
    try:
        del CART_ITEMS[item_id]
    except KeyError:
        return False
    return True


def check_cart_status(item_id):
    """Return whether an item exists in the cart with positive quantity."""
    item = CART_ITEMS.get(item_id)
    return item is not None and item["qty"] > 0


def calculate_discounted_total(item_id, discount_rate=0.10):
    """Calculate an item's discounted price using a validated discount rate."""
    if item_id not in CART_ITEMS:
        raise KeyError(f"Item {item_id} was not found in the cart.")

    if not isinstance(discount_rate, (int, float)):
        raise TypeError("Discount rate must be numeric.")

    if isinstance(discount_rate, bool) or not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    base_price = CART_ITEMS[item_id]["price"]
    return base_price * (1 - discount_rate)


def generate_item_hash(item_id):
    """Generate a SHA-256 digest for an item identifier."""
    return hashlib.sha256(item_id.encode("utf-8")).hexdigest()


def generate_checkout_pin():
    """Generate a four-digit PIN using a cryptographically secure generator."""
    return secrets.randbelow(9000) + 1000


def export_cart_receipt(filename="receipt.txt"):
    """Write the cart contents to a UTF-8 receipt file."""
    with open(filename, "w", encoding="utf-8") as receipt_file:
        for item_id, details in CART_ITEMS.items():
            receipt_file.write(
                f"{item_id}: {details['name']}, "
                f"price={details['price']:.2f}, qty={details['qty']}\n"
            )

    print(f"Receipt saved to: {filename}")


def get_cart_summary(items):
    """Return the total quantity of items with positive quantities."""
    return sum(
        details["qty"]
        for details in items.values()
        if details["qty"] > 0
    )


def main():
    """Run a demonstration of the shopping cart features."""
    add_item_to_cart("ITEM4", "Monitor Stand", 35.0, 1)
    remove_item_from_cart("ITEM2")

    print("Is ITEM1 in cart:", check_cart_status("ITEM1"))
    print("Discounted Price:", calculate_discounted_total("ITEM1", 0.10))
    print("Item Hash:", generate_item_hash("ITEM1"))
    print("Checkout PIN:", generate_checkout_pin())

    export_cart_receipt()
    print("Total items:", get_cart_summary(CART_ITEMS))


if __name__ == "__main__":
    main()
