import json
import os
from datetime import datetime

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


def _path(name):
    return os.path.join(DATA_DIR, f"{name}.json")


def init_storage():
    defaults = {
        "suppliers": [],
        "materials": [],
        "bills": [],
        "price_history": []
    }
    for name, value in defaults.items():
        path = _path(name)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(value, f, indent=2)


def save_data(name, data):
    with open(_path(name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_data(name):
    path = _path(name)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def reset_data():
    save_data("suppliers", [])
    save_data("materials", [])
    save_data("bills", [])
    save_data("price_history", [])


def get_next_id(items, id_key):
    if not items:
        return 1
    return max(item[id_key] for item in items) + 1


def seed_sample_data():
    suppliers = [
        {"supplier_id": 1, "supplier_name": "Apex Building Supply", "contact_person": "Rahul Sharma", "phone": "9876543101", "email": "apex@demo.com", "address": "Dehradun"},
        {"supplier_id": 2, "supplier_name": "Metro Construction Materials", "contact_person": "Ankit Verma", "phone": "9876543102", "email": "metro@demo.com", "address": "Haridwar"},
        {"supplier_id": 3, "supplier_name": "Prime Cement Traders", "contact_person": "Sandeep Rawat", "phone": "9876543103", "email": "prime@demo.com", "address": "Rishikesh"},
        {"supplier_id": 4, "supplier_name": "Granite Edge Suppliers", "contact_person": "Neha Joshi", "phone": "9876543104", "email": "granite@demo.com", "address": "Roorkee"},
        {"supplier_id": 5, "supplier_name": "Urban Steel Depot", "contact_person": "Vikram Negi", "phone": "9876543105", "email": "urbansteel@demo.com", "address": "Dehradun"},
        {"supplier_id": 6, "supplier_name": "National Hardware Mart", "contact_person": "Pooja Thakur", "phone": "9876543106", "email": "national@demo.com", "address": "Saharanpur"},
        {"supplier_id": 7, "supplier_name": "StrongBase Materials", "contact_person": "Amit Bisht", "phone": "9876543107", "email": "strongbase@demo.com", "address": "Delhi"},
        {"supplier_id": 8, "supplier_name": "Foundation Line Traders", "contact_person": "Kavita Rana", "phone": "9876543108", "email": "foundation@demo.com", "address": "Noida"},
        {"supplier_id": 9, "supplier_name": "Crestline Build Supplies", "contact_person": "Mohit Chauhan", "phone": "9876543109", "email": "crestline@demo.com", "address": "Ghaziabad"},
        {"supplier_id": 10, "supplier_name": "BlueRock Infrastructure Co.", "contact_person": "Sneha Kapoor", "phone": "9876543110", "email": "bluerock@demo.com", "address": "Meerut"},
        {"supplier_id": 11, "supplier_name": "Shivam Trade Links", "contact_person": "Shivam Yadav", "phone": "9876543111", "email": "shivam@demo.com", "address": "Lucknow"},
        {"supplier_id": 12, "supplier_name": "Everest Material House", "contact_person": "Renu Singh", "phone": "9876543112", "email": "everest@demo.com", "address": "Kanpur"},
        {"supplier_id": 13, "supplier_name": "Sigma Civil Supplies", "contact_person": "Pranav Kapoor", "phone": "9876543113", "email": "sigma@demo.com", "address": "Chandigarh"},
        {"supplier_id": 14, "supplier_name": "Omkar Industrial Supply", "contact_person": "Omkar Joshi", "phone": "9876543114", "email": "omkar@demo.com", "address": "Jaipur"},
        {"supplier_id": 15, "supplier_name": "Vertex Building Depot", "contact_person": "Meenal Verma", "phone": "9876543115", "email": "vertex@demo.com", "address": "Bhopal"},
        {"supplier_id": 16, "supplier_name": "Haridwar Cement Center", "contact_person": "Deepak Rana", "phone": "9876543116", "email": "haridwarcement@demo.com", "address": "Haridwar"},
        {"supplier_id": 17, "supplier_name": "Royal Hardware Store", "contact_person": "Rohit Saini", "phone": "9876543117", "email": "royal@demo.com", "address": "Dehradun"},
        {"supplier_id": 18, "supplier_name": "Trident Construction Mart", "contact_person": "Neelam Joshi", "phone": "9876543118", "email": "trident@demo.com", "address": "Noida"},
        {"supplier_id": 19, "supplier_name": "PrimeStone Traders", "contact_person": "Yash Gupta", "phone": "9876543119", "email": "primestone@demo.com", "address": "Gurugram"},
        {"supplier_id": 20, "supplier_name": "Aarav Build Supply", "contact_person": "Aarav Bhandari", "phone": "9876543120", "email": "aarav@demo.com", "address": "Dehradun"}
    ]

    materials = [
        {"material_id": 1, "material_name": "OPC Cement 43 Grade", "category": "Cement", "unit": "Bag", "stock_quantity": 420, "current_price": 385, "supplier_id": 1, "last_updated": "2026-04-22"},
        {"material_id": 2, "material_name": "OPC Cement 53 Grade", "category": "Cement", "unit": "Bag", "stock_quantity": 360, "current_price": 405, "supplier_id": 2, "last_updated": "2026-04-22"},
        {"material_id": 3, "material_name": "PPC Cement", "category": "Cement", "unit": "Bag", "stock_quantity": 390, "current_price": 365, "supplier_id": 3, "last_updated": "2026-04-22"},
        {"material_id": 4, "material_name": "White Cement", "category": "Cement", "unit": "Bag", "stock_quantity": 120, "current_price": 620, "supplier_id": 4, "last_updated": "2026-04-22"},
        {"material_id": 5, "material_name": "River Sand", "category": "Sand", "unit": "Ton", "stock_quantity": 780, "current_price": 1550, "supplier_id": 5, "last_updated": "2026-04-22"},
        {"material_id": 6, "material_name": "M-Sand", "category": "Sand", "unit": "Ton", "stock_quantity": 640, "current_price": 1750, "supplier_id": 6, "last_updated": "2026-04-22"},
        {"material_id": 7, "material_name": "Coarse Sand", "category": "Sand", "unit": "Ton", "stock_quantity": 510, "current_price": 1490, "supplier_id": 7, "last_updated": "2026-04-22"},
        {"material_id": 8, "material_name": "10mm Aggregate", "category": "Aggregate", "unit": "Ton", "stock_quantity": 900, "current_price": 1450, "supplier_id": 8, "last_updated": "2026-04-22"},
        {"material_id": 9, "material_name": "20mm Aggregate", "category": "Aggregate", "unit": "Ton", "stock_quantity": 860, "current_price": 1400, "supplier_id": 9, "last_updated": "2026-04-22"},
        {"material_id": 10, "material_name": "Stone Dust", "category": "Aggregate", "unit": "Ton", "stock_quantity": 700, "current_price": 1180, "supplier_id": 10, "last_updated": "2026-04-22"},
        {"material_id": 11, "material_name": "TMT Steel Rod 8mm", "category": "Steel", "unit": "Kg", "stock_quantity": 1200, "current_price": 58, "supplier_id": 11, "last_updated": "2026-04-22"},
        {"material_id": 12, "material_name": "TMT Steel Rod 10mm", "category": "Steel", "unit": "Kg", "stock_quantity": 1150, "current_price": 61, "supplier_id": 12, "last_updated": "2026-04-22"},
        {"material_id": 13, "material_name": "TMT Steel Rod 12mm", "category": "Steel", "unit": "Kg", "stock_quantity": 980, "current_price": 64, "supplier_id": 13, "last_updated": "2026-04-22"},
        {"material_id": 14, "material_name": "TMT Steel Rod 16mm", "category": "Steel", "unit": "Kg", "stock_quantity": 820, "current_price": 66, "supplier_id": 14, "last_updated": "2026-04-22"},
        {"material_id": 15, "material_name": "Binding Wire", "category": "Steel", "unit": "Kg", "stock_quantity": 320, "current_price": 72, "supplier_id": 15, "last_updated": "2026-04-22"},
        {"material_id": 16, "material_name": "Steel Nails", "category": "Steel", "unit": "Kg", "stock_quantity": 250, "current_price": 84, "supplier_id": 16, "last_updated": "2026-04-22"},
        {"material_id": 17, "material_name": "Red Bricks", "category": "Bricks", "unit": "Piece", "stock_quantity": 18000, "current_price": 8, "supplier_id": 17, "last_updated": "2026-04-22"},
        {"material_id": 18, "material_name": "Fly Ash Bricks", "category": "Bricks", "unit": "Piece", "stock_quantity": 22000, "current_price": 10, "supplier_id": 18, "last_updated": "2026-04-22"},
        {"material_id": 19, "material_name": "Clay Bricks", "category": "Bricks", "unit": "Piece", "stock_quantity": 20000, "current_price": 9, "supplier_id": 19, "last_updated": "2026-04-22"},
        {"material_id": 20, "material_name": "AAC Blocks", "category": "Blocks", "unit": "Piece", "stock_quantity": 9600, "current_price": 42, "supplier_id": 20, "last_updated": "2026-04-22"},
        {"material_id": 21, "material_name": "Cement Blocks", "category": "Blocks", "unit": "Piece", "stock_quantity": 8400, "current_price": 38, "supplier_id": 1, "last_updated": "2026-04-22"},
        {"material_id": 22, "material_name": "Paver Blocks", "category": "Blocks", "unit": "Piece", "stock_quantity": 7000, "current_price": 24, "supplier_id": 2, "last_updated": "2026-04-22"},
        {"material_id": 23, "material_name": "Plywood Sheet", "category": "Wood", "unit": "Sheet", "stock_quantity": 140, "current_price": 1750, "supplier_id": 3, "last_updated": "2026-04-22"},
        {"material_id": 24, "material_name": "Shuttering Plywood", "category": "Wood", "unit": "Sheet", "stock_quantity": 110, "current_price": 1850, "supplier_id": 4, "last_updated": "2026-04-22"},
        {"material_id": 25, "material_name": "Door Frame Wood", "category": "Wood", "unit": "Piece", "stock_quantity": 95, "current_price": 2650, "supplier_id": 5, "last_updated": "2026-04-22"},
        {"material_id": 26, "material_name": "PVC Pipe", "category": "Plumbing", "unit": "Meter", "stock_quantity": 520, "current_price": 95, "supplier_id": 6, "last_updated": "2026-04-22"},
        {"material_id": 27, "material_name": "GI Pipe", "category": "Plumbing", "unit": "Meter", "stock_quantity": 410, "current_price": 155, "supplier_id": 7, "last_updated": "2026-04-22"},
        {"material_id": 28, "material_name": "CPVC Pipe", "category": "Plumbing", "unit": "Meter", "stock_quantity": 390, "current_price": 125, "supplier_id": 8, "last_updated": "2026-04-22"},
        {"material_id": 29, "material_name": "Tile Adhesive", "category": "Chemical", "unit": "Bag", "stock_quantity": 210, "current_price": 420, "supplier_id": 9, "last_updated": "2026-04-22"},
        {"material_id": 30, "material_name": "Waterproofing Compound", "category": "Chemical", "unit": "Litre", "stock_quantity": 160, "current_price": 780, "supplier_id": 10, "last_updated": "2026-04-22"},
        {"material_id": 31, "material_name": "Wall Putty", "category": "Chemical", "unit": "Bag", "stock_quantity": 240, "current_price": 360, "supplier_id": 11, "last_updated": "2026-04-22"},
        {"material_id": 32, "material_name": "Paint Primer", "category": "Chemical", "unit": "Litre", "stock_quantity": 180, "current_price": 240, "supplier_id": 12, "last_updated": "2026-04-22"},
        {"material_id": 33, "material_name": "Electrical Conduit Pipe", "category": "Electrical", "unit": "Meter", "stock_quantity": 600, "current_price": 48, "supplier_id": 13, "last_updated": "2026-04-22"},
        {"material_id": 34, "material_name": "Copper Wire 1.5mm", "category": "Electrical", "unit": "Roll", "stock_quantity": 150, "current_price": 940, "supplier_id": 14, "last_updated": "2026-04-22"},
        {"material_id": 35, "material_name": "Switch Board", "category": "Electrical", "unit": "Piece", "stock_quantity": 220, "current_price": 175, "supplier_id": 15, "last_updated": "2026-04-22"},
        {"material_id": 36, "material_name": "Cement Primer", "category": "Chemical", "unit": "Litre", "stock_quantity": 130, "current_price": 510, "supplier_id": 16, "last_updated": "2026-04-22"},
        {"material_id": 37, "material_name": "Glass Wool Sheet", "category": "Insulation", "unit": "Sheet", "stock_quantity": 90, "current_price": 680, "supplier_id": 17, "last_updated": "2026-04-22"},
        {"material_id": 38, "material_name": "Bitumen Sheet", "category": "Roofing", "unit": "Roll", "stock_quantity": 75, "current_price": 1250, "supplier_id": 18, "last_updated": "2026-04-22"},
        {"material_id": 39, "material_name": "MS Pipe", "category": "Plumbing", "unit": "Meter", "stock_quantity": 340, "current_price": 210, "supplier_id": 19, "last_updated": "2026-04-22"},
        {"material_id": 40, "material_name": "Plaster of Paris", "category": "Chemical", "unit": "Bag", "stock_quantity": 260, "current_price": 290, "supplier_id": 20, "last_updated": "2026-04-22"}
    ]

    price_history = []
    history_id = 1
    base_dates = ["2026-03-01", "2026-03-08", "2026-03-15", "2026-03-22", "2026-03-29", "2026-04-05", "2026-04-12", "2026-04-19"]
    price_sets = {
        1: [372, 378, 381, 385, 387, 389, 392, 395],
        2: [395, 398, 400, 405, 408, 410, 412, 415],
        3: [356, 360, 363, 365, 367, 369, 372, 375],
        4: [605, 610, 615, 620, 625, 628, 630, 635],
        5: [1490, 1515, 1530, 1550, 1565, 1580, 1590, 1605],
        6: [1680, 1700, 1730, 1750, 1765, 1780, 1795, 1810],
        7: [1450, 1460, 1475, 1490, 1500, 1510, 1520, 1535],
        8: [1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490],
        9: [1385, 1390, 1395, 1400, 1405, 1410, 1415, 1420],
        10: [1160, 1170, 1180, 1185, 1190, 1195, 1200, 1205],
        11: [55, 56, 57, 58, 59, 60, 61, 62],
        12: [58, 59, 60, 61, 62, 63, 64, 65],
        13: [61, 62, 63, 64, 65, 66, 67, 68],
        14: [63, 64, 65, 66, 67, 68, 69, 70],
        15: [68, 69, 70, 72, 73, 74, 75, 76],
        16: [80, 81, 82, 84, 85, 86, 87, 88],
        17: [7.5, 7.6, 7.7, 8.0, 8.1, 8.2, 8.3, 8.4],
        18: [9.5, 9.6, 9.7, 10.0, 10.1, 10.2, 10.3, 10.4],
        19: [8.4, 8.5, 8.6, 8.8, 8.9, 9.0, 9.1, 9.2],
        20: [40, 40.5, 41, 42, 42.5, 43, 43.5, 44],
        21: [36, 36.5, 37, 38, 38.5, 39, 39.5, 40],
        22: [22, 22.5, 23, 24, 24.5, 25, 25.5, 26],
        23: [1650, 1680, 1700, 1750, 1765, 1775, 1785, 1800],
        24: [1750, 1780, 1800, 1850, 1865, 1875, 1890, 1900],
        25: [2550, 2575, 2600, 2650, 2675, 2690, 2700, 2725],
        26: [92, 93, 94, 95, 96, 97, 98, 99],
        27: [150, 152, 153, 155, 156, 157, 158, 160],
        28: [120, 121, 122, 125, 126, 127, 128, 130],
        29: [400, 405, 410, 420, 425, 430, 435, 440],
        30: [750, 760, 770, 780, 790, 800, 810, 820],
        31: [340, 345, 350, 360, 365, 370, 375, 380],
        32: [220, 225, 230, 240, 245, 250, 255, 260],
        33: [44, 45, 46, 48, 49, 50, 51, 52],
        34: [910, 920, 930, 940, 950, 960, 970, 980],
        35: [165, 168, 170, 175, 178, 180, 182, 185],
        36: [480, 490, 500, 510, 520, 530, 540, 550],
        37: [650, 655, 660, 680, 690, 700, 710, 720],
        38: [1180, 1200, 1220, 1250, 1260, 1270, 1280, 1290],
        39: [200, 202, 205, 210, 212, 215, 218, 220],
        40: [270, 275, 280, 290, 295, 300, 305, 310]
    }

    for material_id, prices in price_sets.items():
        for d, p in zip(base_dates, prices):
            price_history.append({
                "history_id": history_id,
                "material_id": material_id,
                "price": p,
                "changed_on": d
            })
            history_id += 1

    save_data("suppliers", suppliers)
    save_data("materials", materials)
    save_data("price_history", price_history)
    save_data("bills", [])


def get_supplier_name(supplier_id):
    suppliers = load_data("suppliers")
    for supplier in suppliers:
        if supplier["supplier_id"] == supplier_id:
            return supplier["supplier_name"]
    return "Unknown Supplier"


def add_supplier(supplier_name, contact_person, phone, email, address):
    suppliers = load_data("suppliers")
    new_id = get_next_id(suppliers, "supplier_id")
    suppliers.append({
        "supplier_id": new_id,
        "supplier_name": supplier_name.strip(),
        "contact_person": contact_person.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "address": address.strip()
    })
    save_data("suppliers", suppliers)
    return new_id


def update_supplier(supplier_id, supplier_name, contact_person, phone, email, address):
    suppliers = load_data("suppliers")
    for supplier in suppliers:
        if supplier["supplier_id"] == supplier_id:
            supplier["supplier_name"] = supplier_name.strip()
            supplier["contact_person"] = contact_person.strip()
            supplier["phone"] = phone.strip()
            supplier["email"] = email.strip()
            supplier["address"] = address.strip()
            save_data("suppliers", suppliers)
            return True
    return False


def delete_supplier(supplier_id):
    suppliers = load_data("suppliers")
    materials = load_data("materials")
    if any(material["supplier_id"] == supplier_id for material in materials):
        raise ValueError("This supplier is linked to existing materials.")
    suppliers = [supplier for supplier in suppliers if supplier["supplier_id"] != supplier_id]
    save_data("suppliers", suppliers)
    return True


def add_material(material_name, category, unit, stock_quantity, current_price, supplier_id):
    materials = load_data("materials")
    new_id = get_next_id(materials, "material_id")
    materials.append({
        "material_id": new_id,
        "material_name": material_name.strip(),
        "category": category.strip(),
        "unit": unit.strip(),
        "stock_quantity": int(stock_quantity),
        "current_price": float(current_price),
        "supplier_id": supplier_id,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    })
    save_data("materials", materials)
    return new_id


def update_material(material_id, material_name, category, unit, stock_quantity, current_price, supplier_id):
    materials = load_data("materials")
    for material in materials:
        if material["material_id"] == material_id:
            material["material_name"] = material_name.strip()
            material["category"] = category.strip()
            material["unit"] = unit.strip()
            material["stock_quantity"] = int(stock_quantity)
            material["current_price"] = float(current_price)
            material["supplier_id"] = supplier_id
            material["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            save_data("materials", materials)
            return True
    return False


def delete_material(material_id):
    materials = load_data("materials")
    materials = [material for material in materials if material["material_id"] != material_id]
    save_data("materials", materials)
    return True


def create_bill(customer_name, customer_phone, cart_items):
    customer_name = customer_name.strip()
    customer_phone = customer_phone.strip()

    if not customer_name or not customer_phone:
        raise ValueError("Customer name and phone are required.")
    if not cart_items:
        raise ValueError("Cart is empty.")

    materials = load_data("materials")
    bills = load_data("bills")
    material_map = {material["material_id"]: material for material in materials}

    merged_cart = {}
    for item in cart_items:
        material_id = int(item["material_id"])
        quantity = int(item["quantity"])
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        merged_cart[material_id] = merged_cart.get(material_id, 0) + quantity

    bill_items = []
    total_amount = 0.0

    for material_id, qty in merged_cart.items():
        material = material_map.get(material_id)
        if not material:
            raise ValueError("One of the selected materials no longer exists.")

        if material["stock_quantity"] < qty:
            raise ValueError(f"Not enough stock for {material['material_name']}.")

        unit_price = float(material["current_price"])
        line_total = round(qty * unit_price, 2)
        total_amount += line_total

        material["stock_quantity"] -= qty
        material["last_updated"] = datetime.now().strftime("%Y-%m-%d")

        bill_items.append({
            "material_id": material_id,
            "material_name": material["material_name"],
            "quantity": qty,
            "unit_price": unit_price,
            "line_total": line_total
        })

    save_data("materials", materials)

    new_bill_id = get_next_id(bills, "bill_id")
    bill = {
        "bill_id": new_bill_id,
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "bill_date": datetime.now().strftime("%Y-%m-%d"),
        "items": bill_items,
        "total_amount": round(total_amount, 2)
    }

    bills.append(bill)
    save_data("bills", bills)
    return bill