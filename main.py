from flask import Flask, render_template, jsonify, request, abort
from database import Database
app = Flask(__name__)
db = Database()

# pages


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/setting')
def settings():
    return render_template('setting.html')


# price service

@app.route('/get-price')
def get_price():
    price = db.harga_collection.find({}, {'_id': False})
    price_list = list(price)
    return jsonify(price_list)


@app.route('/edit-price/<string:paket>', methods=['PUT'])
def edit_price(paket):
    try:
        updated_data = request.json
        result = db.harga_collection.update_many(
            {'paket': paket}, {'$set': updated_data})

        if result.modified_count > 0:
            return jsonify({"status": "success", "message": f"Edit harga {paket} berhasl "})
        else:
            return jsonify({"status": "error", "message": f"Edit harga  {paket} gagal"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# order service

@app.route('/get-orders', methods=['GET'])
def get_orders():
    orders = db.order_collection.find({}, {'_id': 0})  # not include _id
    order_list = list(orders)
    return jsonify(order_list)


@app.route('/add-orders', methods=['POST'])
def add_order():
    if request.is_json:
        order_data = request.json

        last_order = db.order_collection.find_one(sort=[("id", -1)])
        new_id = last_order["id"] + 1 if last_order else 1

        order_data["id"] = new_id

        db.order_collection.insert_one(order_data)
        return jsonify({"status": "success", "id": new_id})
    else:
        return jsonify({"status": "error", "message": "error"}), 400


@app.route('/delete-orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        result = db.order_collection.delete_one({'id': order_id})
        if result.deleted_count == 1:
            return jsonify({"status": "success", "message": f"Order ID {order_id} dihapus"})
        else:
            return jsonify({"status": "error", "message": f"tidak ada order ditemukan {order_id}"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/edit-orders/<int:order_id>', methods=['PUT'])
def edit_order(order_id):
    try:
        updated_data = request.json

        if 'id' in updated_data and updated_data['id'] != order_id:
            return jsonify({"status": "errormiss", "message": "perbedaan ID pada editing"}), 400

        result = db.order_collection.update_one(
            {'id': order_id}, {'$set': updated_data})

        if result.modified_count == 1:
            return jsonify({"status": "success", "message": f"Order ID {order_id} ter update"})
        else:
            return jsonify({"status": "error", "message": f"tidak ada order ditemukan{order_id}"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
