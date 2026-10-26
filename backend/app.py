from flask import Flask, jsonify, request

app = Flask(__name__)

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

@app.route("/health", methods=['GET'])
def health():
  return jsonify(status="ok")
  
@app.route("/api/inventory", methods=['POST'])
def create_item():
  data = request.get_json(silent=True) or {}
  name = str(data.get("name", "")).strip()
  quantity = data.get("quantity")

  # Validamos antes de guardar
  if not name or not isinstance(quantity, int) or quantity < 0:
    return jsonify(error="Se requiere 'name' (texto) y 'quantity' (entero >= 0)"), 400

  new_id = max((item["id"] for item in inventory_items), default=0) + 1
  item = {"id": new_id, "name": name, "quantity": quantity}
  inventory_items.append(item)
  return jsonify(item), 201
  
@app.route("/api/inventory/<int:item_id>", methods=['PUT'])
def update_item(item_id):
  data = request.get_json(silent=True) or {}
  name = str(data.get("name", "")).strip()
  quantity = data.get("quantity")

  # Validamos antes de guardar
  if not name or not isinstance(quantity, int) or quantity < 0:
    return jsonify(error="Se requiere 'name' (texto) y 'quantity' (entero >= 0)"), 400

  # Buscamos el producto con ese id (None si no existe)
  item = next((item for item in inventory_items if item["id"] == item_id), None)
  if item is None:
    return jsonify(error=f"No existe el producto {item_id}"), 404

  # Actualizamos el mismo diccionario que está en la lista
  item["name"] = name
  item["quantity"] = quantity
  return jsonify(item), 200

@app.route("/api/inventory/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
  # Buscamos el producto con ese id (None si no existe)
  item = next((item for item in inventory_items if item["id"] == item_id), None)
  if item is None:
    return jsonify(error=f"No existe el producto {item_id}"), 404
  
  inventory_items.remove(item)
  return jsonify(item), 200
