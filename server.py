from flask import Flask, render_template, request
import json
from config import db
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.get("/api/about")
def about():
    name = {"name" : "Rafael Cabrera"}
    return name


@app.get("/api/students")
def students():
    students = ["Jeffrey", "George", "Nar", "Rafael", "Isai" "Erick"]
    return students


products = []


@app.get("/api/products")
def get_products():
    products = []
    cursor = db.products.find()
    for product in cursor:
        products.append(fix_id(product))
    print("Products endpoint accessed")
    return json.dumps(products)


@app.get("/api/categories")
def get_categories():
    categories = []
    cursor = db.products.find({})
    for product in cursor:
        cat = product["category"]
        # Verificamos si la categoría ya está en la lista
        if not any(item['category'] == cat for item in categories):
            # Añadimos un objeto con category e image
            categories.append({
                "category": cat,
                "image": f"images/Filters/{cat}.webp"
            })
    
    print("Categories endpoint accessed")
    return json.dumps(categories)


@app.get("/api/reports/total")
def get_total_prices():
    total = 0
    cursor = db.products.find({})
    for product in cursor:
        total += product["price"]
    
    print("Total prices endpoint accessed")
    return json.dumps(total)


def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

#POST
@app.post("/api/products")
def post_products():
    item = request.get_json()
    print(item)

    db.products.insert_one(item)
    print(item)
    return json.dumps(fix_id(item))

# PUT
@app.put("/api/products/<int:index>")
def put_products(index):
    updated_item = request.get_json()
    if len(products) > index >= 0:
        products[index] = updated_item
        return json.dumps(updated_item)
    else:
        return "Index does not exist"

#DELETE
@app.delete("/api/products/<int:index>")
def delete_product(index):
    delete_item = request.get_json()
    if 0<= index < len(products):
        delete_item = products.pop(index)
        return json.dumps(delete_item)
    else:
        return "That item does not exist"


@app.patch("/api/products/<int:index>")
def patch_product(index):
    patch_item = request.get_json()
    if 0<= index < len(products):
        products(index).update(patch_item)
        return json.dumps(products)
    else:
        return "That item does not exist"


@app.get("/greet/<name>")
def asd_api(name):
    
    print("Greet endpoint accessed")
    
    #return "Hello " + name
    return f"Hello {name}"


@app.post("/api/coupons")
def create_coupon():
    coupon = request.get_json()
    print(coupon)

    db.coupons.insert_one(coupon)
    print(coupon)
    return json.dumps(fix_id(coupon))


@app.get("/api/coupons")
def get_coupon():
    coupon = []
    cursor = db.coupons.find()
    for coup in cursor:
        coupon.append(fix_id(coup))
    print("Coupons endpoint accessed")
    return json.dumps(coupon)


app.run(debug=True, port=8000)