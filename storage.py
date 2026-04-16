import json
import os
from datetime import datetime

# All our JSON files live inside this folder.
DATA_DIR = "data"

# These are the files the app uses to save data.
FILES = {
    "suppliers": os.path.join(DATA_DIR, "suppliers.json"),
    "materials": os.path.join(DATA_DIR, "materials.json"),
    "bills": os.path.join(DATA_DIR, "bills.json"),
    "price_history": os.path.join(DATA_DIR, "price_history.json"),
}


def current_timestamp():
    # Keeps all date and time values in one consistent format.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_storage():
    # Make sure the data folder exists.
    os.makedirs(DATA_DIR, exist_ok=True)

    # Create each JSON file if it is missing.
    # We start with an empty list because each file stores multiple records.
    for file_path in FILES.values():
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)


def load_data(name):
    # Read data from one JSON file and return it as a Python list.
    init_storage()
    with open(FILES[name], "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(name, data):
    # Save the updated list back into the matching JSON file.
    with open(FILES[name], "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def generate_id(records, key):
    # If there are no records yet, start IDs from 1.
    # Otherwise, take the biggest existing ID and add 1.
    if not records:
        return 1
    return max(item[key] for item in records) + 1


def find_record_by_id(records, key, value):
    # Small helper to avoid repeating the same search loop everywhere.
    for record in records:
        if record[key] == value:
            return record
    return None


def get_all_suppliers():
    # Show newest suppliers first.
    suppliers = load_data("suppliers")
    return list(reversed(suppliers))


def add_supplier(supplier_name, contact_person, phone, email, address):
    suppliers = load_data("suppliers")

    new_supplier = {
        "supplier_id": generate_id(suppliers, "supplier_id"),
        "supplier_name": supplier_name.strip(),
        "contact_person": contact_person.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "address": address.strip(),
        "created_at": current_timestamp()
    }

    suppliers.append(new_supplier)
    save_data("suppliers", suppliers)


def update_supplier(supplier_id, supplier_name, contact_person, phone, email, address):
    suppliers = load_data("suppliers")
    supplier = find_record_by_id(suppliers, "supplier_id", supplier_id)

    if supplier is None:
        raise ValueError("Supplier not found.")

    supplier["supplier_name"] = supplier_name.strip()
    supplier["contact_person"] = contact_person.strip()
    supplier["phone"] = phone.strip()
    supplier["email"] = email.strip()
    supplier["address"] = address.strip()

    save_data("suppliers", suppliers)


def delete_supplier(supplier_id):
    suppliers = load_data("suppliers")
    materials = load_data("materials")

    # Don't allow deleting a supplier if some material still points to it.
    linked_materials = [material for material in materials if material["supplier_id"] == supplier_id]
    if linked_materials:
        raise ValueError("Cannot delete supplier because materials are linked to it.")

    updated_suppliers = [supplier for supplier in suppliers if supplier["supplier_id"] != supplier_id]
    save_data("suppliers", updated_suppliers)


def get_all_materials():
    # Show newest materials first.
    materials = load_data("materials")
    return list(reversed(materials))


def add_material(material_name, category, unit, stock_quantity, current_price, supplier_id):
    materials = load_data("materials")

    new_material = {
        "material_id": generate_id(materials, "material_id"),
        "material_name": material_name.strip(),
        "category": category.strip(),
        "unit": unit.strip(),
        "stock_quantity": int(stock_quantity),
        "current_price": float(current_price),
        "supplier_id": supplier_id,
        "last_updated": current_timestamp()
    }

    materials.append(new_material)
    save_data("materials", materials)

    # Save the first price too, so analytics and prediction already have a starting point.
    add_price_history(new_material["material_id"], float(current_price))


def update_material(material_id, material_name, category, unit, stock_quantity, current_price, supplier_id):
    materials = load_data("materials")
    material = find_record_by_id(materials, "material_id", material_id)

    if material is None:
        raise ValueError("Material not found.")

    old_price = float(material["current_price"])
    new_price = float(current_price)

    material["material_name"] = material_name.strip()
    material["category"] = category.strip()
    material["unit"] = unit.strip()
    material["stock_quantity"] = int(stock_quantity)
    material["current_price"] = new_price
    material["supplier_id"] = supplier_id
    material["last_updated"] = current_timestamp()

    save_data("materials", materials)

    # Only add a new history entry if the price actually changed.
    if old_price != new_price:
        add_price_history(material_id, new_price)


def delete_material(material_id):
    materials = load_data("materials")
    price_history = load_data("price_history")

    # Remove the material itself.
    updated_materials = [material for material in materials if material["material_id"] != material_id]

    # Also remove old price history for that material.
    updated_history = [record for record in price_history if record["material_id"] != material_id]

    save_data("materials", updated_materials)
    save_data("price_history", updated_history)


def add_price_history(material_id, price):
    history = load_data("price_history")

    new_record = {
        "history_id": generate_id(history, "history_id"),
        "material_id": material_id,
        "price": float(price),
        "changed_on": current_timestamp()
    }

    history.append(new_record)
    save_data("price_history", history)


def get_price_history():
    return load_data("price_history")


def get_supplier_name(supplier_id):
    suppliers = load_data("suppliers")
    supplier = find_record_by_id(suppliers, "supplier_id", supplier_id)

    if supplier:
        return supplier["supplier_name"]

    return "Unknown"


def create_bill(customer_name, customer_phone, cart_items):
    # Customer name is required because every bill should belong to someone.
    if not customer_name.strip():
        raise ValueError("Customer name is required.")

    materials = load_data("materials")
    bills = load_data("bills")

    total_amount = 0
    bill_items = []

    # First, check that every cart item is valid and calculate totals.
    for cart_item in cart_items:
        material_id = cart_item["material_id"]
        quantity = int(cart_item["quantity"])

        material = find_record_by_id(materials, "material_id", material_id)

        if material is None:
            raise ValueError("Material not found.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if quantity > material["stock_quantity"]:
            raise ValueError(f"Not enough stock for {material['material_name']}.")

        unit_price = float(material["current_price"])
        line_total = quantity * unit_price
        total_amount += line_total

        bill_items.append({
            "material_id": material["material_id"],
            "material_name": material["material_name"],
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total
        })

    # If everything is valid, update stock.
    for cart_item in cart_items:
        material = find_record_by_id(materials, "material_id", cart_item["material_id"])
        material["stock_quantity"] -= int(cart_item["quantity"])
        material["last_updated"] = current_timestamp()

    # Now create the final bill object.
    new_bill = {
        "bill_id": generate_id(bills, "bill_id"),
        "customer_name": customer_name.strip(),
        "customer_phone": customer_phone.strip(),
        "bill_date": current_timestamp(),
        "total_amount": total_amount,
        "items": bill_items
    }

    bills.append(new_bill)

    # Save both the updated stock and the new bill.
    save_data("materials", materials)
    save_data("bills", bills)

    return new_bill