import json
import os
from datetime import datetime

DATA_DIR = "data"

FILES = {
    "suppliers": os.path.join(DATA_DIR, "suppliers.json"),
    "materials": os.path.join(DATA_DIR, "materials.json"),
    "bills": os.path.join(DATA_DIR, "bills.json"),
    "price_history": os.path.join(DATA_DIR, "price_history.json"),
}


def init_storage():
    os.makedirs(DATA_DIR, exist_ok=True)

    for file_path in FILES.values():
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)


def load_data(name):
    with open(FILES[name], "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(name, data):
    with open(FILES[name], "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def generate_id(records, key):
    if not records:
        return 1
    return max(item[key] for item in records) + 1


def add_supplier(supplier_name, contact_person, phone, email, address):
    suppliers = load_data("suppliers")

    new_supplier = {
        "supplier_id": generate_id(suppliers, "supplier_id"),
        "supplier_name": supplier_name,
        "contact_person": contact_person,
        "phone": phone,
        "email": email,
        "address": address,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    suppliers.append(new_supplier)
    save_data("suppliers", suppliers)


def update_supplier(supplier_id, supplier_name, contact_person, phone, email, address):
    suppliers = load_data("suppliers")

    for supplier in suppliers:
        if supplier["supplier_id"] == supplier_id:
            supplier["supplier_name"] = supplier_name
            supplier["contact_person"] = contact_person
            supplier["phone"] = phone
            supplier["email"] = email
            supplier["address"] = address
            break

    save_data("suppliers", suppliers)


def delete_supplier(supplier_id):
    suppliers = load_data("suppliers")
    materials = load_data("materials")

    linked_materials = [m for m in materials if m["supplier_id"] == supplier_id]
    if linked_materials:
        raise ValueError("Cannot delete supplier because materials are linked to it.")

    updated_suppliers = [s for s in suppliers if s["supplier_id"] != supplier_id]
    save_data("suppliers", updated_suppliers)


def add_material(material_name, category, unit, stock_quantity, current_price, supplier_id):
    materials = load_data("materials")

    new_material = {
        "material_id": generate_id(materials, "material_id"),
        "material_name": material_name,
        "category": category,
        "unit": unit,
        "stock_quantity": int(stock_quantity),
        "current_price": float(current_price),
        "supplier_id": supplier_id,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    materials.append(new_material)
    save_data("materials", materials)
    add_price_history(new_material["material_id"], float(current_price))


def update_material(material_id, material_name, category, unit, stock_quantity, current_price, supplier_id):
    materials = load_data("materials")

    for material in materials:
        if material["material_id"] == material_id:
            old_price = material["current_price"]

            material["material_name"] = material_name
            material["category"] = category
            material["unit"] = unit
            material["stock_quantity"] = int(stock_quantity)
            material["current_price"] = float(current_price)
            material["supplier_id"] = supplier_id
            material["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if old_price != float(current_price):
                add_price_history(material_id, float(current_price))
            break

    save_data("materials", materials)


def delete_material(material_id):
    materials = load_data("materials")
    updated_materials = [m for m in materials if m["material_id"] != material_id]
    save_data("materials", updated_materials)


def add_price_history(material_id, price):
    history = load_data("price_history")

    new_record = {
        "history_id": generate_id(history, "history_id"),
        "material_id": material_id,
        "price": float(price),
        "changed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(new_record)
    save_data("price_history", history)


def get_supplier_name(supplier_id):
    suppliers = load_data("suppliers")
    for supplier in suppliers:
        if supplier["supplier_id"] == supplier_id:
            return supplier["supplier_name"]
    return "Unknown"


def create_bill(customer_name, customer_phone, cart_items):
    if not customer_name.strip():
        raise ValueError("Customer name is required.")

    materials = load_data("materials")
    bills = load_data("bills")

    total_amount = 0
    bill_items = []

    for cart_item in cart_items:
        material_id = cart_item["material_id"]
        quantity = int(cart_item["quantity"])

        material = None
        for item in materials:
            if item["material_id"] == material_id:
                material = item
                break

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

    for cart_item in cart_items:
        material_id = cart_item["material_id"]
        quantity = int(cart_item["quantity"])

        for material in materials:
            if material["material_id"] == material_id:
                material["stock_quantity"] -= quantity
                material["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break

    new_bill = {
        "bill_id": generate_id(bills, "bill_id"),
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "bill_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_amount": total_amount,
        "items": bill_items
    }

    bills.append(new_bill)

    save_data("materials", materials)
    save_data("bills", bills)

    return new_bill