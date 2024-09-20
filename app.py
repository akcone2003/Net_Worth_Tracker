from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Asset Model
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # E.g., 'Real Estate', 'Stocks'

# Define the Liability Model
class Liability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    liability_type = db.Column(db.String(50), nullable=False)  # E.g., 'Mortgage', 'Car Loan'

# Define the Spending Model
class Spending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)  # E.g., 'Food', 'Entertainment'
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(50), nullable=False)  # You could use datetime for better accuracy

# Manually create tables when the app starts
with app.app_context():
    db.create_all()

# Example endpoint for testing
@app.route('/')
def home():
    return "Net Worth Tracker API is running!"


# Adding routes for assets, liabilities, and expenses
@app.route('/assets', methods=['POST'])
def add_asset():
    data = request.get_json()
    new_asset = Asset(name=data['name'], value=data['value'], asset_type=data['asset_type'])
    db.session.add(new_asset)
    db.session.commit()
    return jsonify({'message': 'Asset added successfully'}), 201

# Route to add a liability
@app.route('/liabilities', methods=['POST'])
def add_liability():
    data = request.get_json()
    new_liability = Liability(name=data['name'], value=data['value'], liability_type=data['liability_type'])
    db.session.add(new_liability)
    db.session.commit()
    return jsonify({'message': 'Liability added successfully'}), 201

# Route to add a spending
@app.route('/spending', methods=['POST'])
def add_spending():
    data = request.get_json()
    new_spending = Spending(category=data['category'], amount=data['amount'], date=data['date'])
    db.session.add(new_spending)
    db.session.commit()
    return jsonify({'message': 'Spending added successfully'}), 201

# GET
# Route to get all assets
@app.route('/assets', methods=['GET'])
def get_assets():
    assets = Asset.query.all()
    asset_list = [{'id': asset.id, 'name': asset.name, 'value': asset.value, 'type': asset.asset_type} for asset in assets]
    return jsonify(asset_list), 200

# Route to get all liabilities
@app.route('/liabilities', methods=['GET'])
def get_liabilities():
    liabilities = Liability.query.all()
    liability_list = [{'id': liability.id, 'name': liability.name, 'value': liability.value, 'type': liability.liability_type} for liability in liabilities]
    return jsonify(liability_list), 200

# Route to get all spending
@app.route('/spending', methods=['GET'])
def get_spending():
    spending = Spending.query.all()
    spending_list = [{'id': spend.id, 'category': spend.category, 'amount': spend.amount, 'date': spend.date} for spend in spending]
    return jsonify(spending_list), 200


# Route to calculate net worth
@app.route('/net_worth', methods=['GET'])
def get_net_worth():
    total_assets = db.session.query(db.func.sum(Asset.value)).scalar() or 0
    total_liabilities = db.session.query(db.func.sum(Liability.value)).scalar() or 0
    net_worth = total_assets - total_liabilities

    return jsonify({
        'net_worth': net_worth,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities
    })

# CRUD Operations
@app.route('/assets/<int:id>', methods=['PUT'])
def update_asset(id):
    data = request.get_json()
    asset = Asset.query.get(id)

    if asset:
        asset.name = data['name']
        asset.value = data['value']
        asset.asset_type = data['asset_type']
        db.session.commit()
        return jsonify({'message': 'Asset updated successfully'}), 200
    else:
        return jsonify({'message': 'Asset not found'}), 404


@app.route('/assets/<int:id>', methods=['DELETE'])
def delete_asset(id):
    asset = Asset.query.get(id)

    if asset:
        db.session.delete(asset)
        db.session.commit()
        return jsonify({'message': 'Asset deleted successfully'}), 200
    else:
        return jsonify({'message': 'Asset not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)