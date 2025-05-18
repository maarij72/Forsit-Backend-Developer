from database import init_db
from database import SessionLocal
import models
from datetime import datetime


def populate():
    init_db()
    db = SessionLocal()
    # Create categories
    categories = ["Electronics", "Books", "Toys", "Home", "Clothing"]
    category_objs = []
    for cat in categories:
        c = models.Category(name=cat)
        db.add(c)
        category_objs.append(c)
    db.commit()
    for c in category_objs:
        db.refresh(c)

    # Map names to ids
    category_map = {c.name: c.id for c in category_objs}

    # Create products
    products_data = [
        {
            "name": "Smartphone",
            "description": "Latest model smartphone",
            "price": 699.0,
            "category": "Electronics",
        },
        {
            "name": "Laptop",
            "description": "High performance laptop",
            "price": 999.0,
            "category": "Electronics",
        },
        {
            "name": "Novel",
            "description": "Bestselling fiction novel",
            "price": 19.99,
            "category": "Books",
        },
        {
            "name": "Action Figure",
            "description": "Popular action figure toy",
            "price": 15.99,
            "category": "Toys",
        },
        {
            "name": "Blender",
            "description": "Kitchen blender",
            "price": 49.99,
            "category": "Home",
        },
    ]
    product_objs = []
    for pd in products_data:
        p = models.Product(
            name=pd["name"],
            description=pd["description"],
            price=pd["price"],
            category_id=category_map[pd["category"]],
        )
        db.add(p)
        product_objs.append(p)
    db.commit()
    for p in product_objs:
        db.refresh(p)

    # Map product names to ids
    product_map = {p.name: p.id for p in product_objs}

    # Create inventory for each product in Amazon and Walmart
    inventory_entries = [
        {"product": "Smartphone", "channel": "Amazon", "quantity": 50, "reorder": 10},
        {"product": "Smartphone", "channel": "Walmart", "quantity": 30, "reorder": 10},
        {"product": "Laptop", "channel": "Amazon", "quantity": 20, "reorder": 5},
        {"product": "Laptop", "channel": "Walmart", "quantity": 15, "reorder": 5},
        {"product": "Novel", "channel": "Amazon", "quantity": 100, "reorder": 20},
        {"product": "Novel", "channel": "Walmart", "quantity": 120, "reorder": 20},
        {
            "product": "Action Figure",
            "channel": "Amazon",
            "quantity": 60,
            "reorder": 10,
        },
        {
            "product": "Action Figure",
            "channel": "Walmart",
            "quantity": 40,
            "reorder": 10,
        },
        {"product": "Blender", "channel": "Amazon", "quantity": 10, "reorder": 3},
        {"product": "Blender", "channel": "Walmart", "quantity": 12, "reorder": 3},
        {"product": "TV", "channel": "Walmart", "quantity": 12, "reorder": 50},
    ]
    inventory_objs = []
    for inv in inventory_entries:
        i = models.Inventory(
            product_id=product_map[inv["product"]],
            channel=inv["channel"],
            quantity=inv["quantity"],
            reorder_level=inv["reorder"],
        )
        db.add(i)
        inventory_objs.append(i)
    db.commit()
    for i in inventory_objs:
        db.refresh(i)

    # Create initial inventory history (initial stock)
    for inv in inventory_objs:
        hist = models.InventoryHistory(
            inventory_id=inv.id, change_qty=inv.quantity, comment="Initial stock"
        )
        db.add(hist)
    db.commit()

    # Create sales
    sales_data = [
        # product, channel, quantity, price, sale_date (YMD)
        {
            "product": "Smartphone",
            "channel": "Amazon",
            "quantity": 2,
            "price": 699.0,
            "date": "2025-05-01",
        },
        {
            "product": "Smartphone",
            "channel": "Walmart",
            "quantity": 1,
            "price": 679.0,
            "date": "2025-05-02",
        },
        {
            "product": "Smartphone",
            "channel": "Amazon",
            "quantity": 3,
            "price": 699.0,
            "date": "2025-05-03",
        },
        {
            "product": "Laptop",
            "channel": "Amazon",
            "quantity": 1,
            "price": 999.0,
            "date": "2025-05-04",
        },
        {
            "product": "Laptop",
            "channel": "Walmart",
            "quantity": 2,
            "price": 989.0,
            "date": "2025-05-05",
        },
        {
            "product": "Novel",
            "channel": "Walmart",
            "quantity": 5,
            "price": 19.99,
            "date": "2025-05-06",
        },
        {
            "product": "Action Figure",
            "channel": "Amazon",
            "quantity": 2,
            "price": 15.99,
            "date": "2025-05-07",
        },
        {
            "product": "Action Figure",
            "channel": "Walmart",
            "quantity": 3,
            "price": 14.99,
            "date": "2025-05-08",
        },
        {
            "product": "Blender",
            "channel": "Amazon",
            "quantity": 1,
            "price": 49.99,
            "date": "2025-05-09",
        },
        {
            "product": "Blender",
            "channel": "Walmart",
            "quantity": 2,
            "price": 47.99,
            "date": "2025-05-10",
        },
        {
            "product": "Smartphone",
            "channel": "Amazon",
            "quantity": 1,
            "price": 699.0,
            "date": "2024-12-25",
        },
    ]
    for sd in sales_data:
        sale = models.Sale(
            product_id=product_map[sd["product"]],
            channel=sd["channel"],
            quantity=sd["quantity"],
            price=sd["price"],
            sale_date=datetime.fromisoformat(sd["date"]),
        )
        db.add(sale)
    db.commit()

    print("Database has been populated with demo data.")


if __name__ == "__main__":
    populate()
