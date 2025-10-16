from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

inventory_items = [
  { "id": 1, "name": 'Laptop', "quantity": 15 },
  { "id": 2, "name": 'Teclado', "quantity": 50 },
  { "id": 3, "name": 'Mouse', "quantity": 75 },
  { "id": 4, "name": 'Monitor', "quantity": 25 },
  { "id": 5, "name": 'Impresora', "quantity": 10 },
  { "id": 6, "name": 'Escáner', "quantity": 5 },
  { "id": 7, "name": 'Proyector', "quantity": 8 },
  { "id": 8, "name": 'Router', "quantity": 20 },
  { "id": 9, "name": 'Switch', "quantity": 12 },
  { "id": 10, "name": 'Servidor', "quantity": 3 }
]
@app.route("/api/inventory", methods=['GET'])
def get_inventory():
  return jsonify(inventory_items)
