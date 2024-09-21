from flask import Flask, jsonify, request, render_template
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

# Model for Monthly Income and Monthly Spending
class MonthlyIncome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

class MonthlySpending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Serve the index.html template
@app.route('/')
def home():
    return render_template('index.html')

# Route to add an asset
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

# Route to add monthly income
@app.route('/monthly_income', methods=['POST'])
def add_monthly_income():
    data = request.get_json()
    try:
        new_income = MonthlyIncome(amount=data['amount'])
        db.session.add(new_income)
        db.session.commit()
        return jsonify({'message': 'Monthly income added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error occurred: {e}'}), 500

# Route to add monthly spending
@app.route('/monthly_spending', methods=['POST'])
def add_monthly_spending():
    data = request.get_json()
    try:
        new_spending = MonthlySpending(category=data['category'], amount=data['amount'])
        db.session.add(new_spending)
        db.session.commit()
        return jsonify({'message': 'Monthly spending added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error occurred: {e}'}), 500

# Route to get total monthly income and spending
@app.route('/monthly_income_spending', methods=['GET'])
def get_monthly_income_spending():
    total_income = db.session.query(db.func.sum(MonthlyIncome.amount)).scalar() or 0
    total_spending = db.session.query(db.func.sum(MonthlySpending.amount)).scalar() or 0
    return jsonify({'total_income': total_income, 'total_spending': total_spending})

# Route to calculate net worth (assets vs liabilities)
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

# Route to get all assets (GET request)
@app.route('/assets', methods=['GET'])
def get_assets():
    assets = Asset.query.all()
    asset_list = [{'id': asset.id, 'name': asset.name, 'value': asset.value, 'type': asset.asset_type} for asset in assets]
    return jsonify(asset_list), 200

# Route to get all liabilities (GET request)
@app.route('/liabilities', methods=['GET'])
def get_liabilities():
    liabilities = Liability.query.all()
    liability_list = [{'id': liability.id, 'name': liability.name, 'value': liability.value, 'type': liability.liability_type} for liability in liabilities]
    return jsonify(liability_list), 200

# CRUD Operations (Update and Delete Assets)
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

@app.route('/liabilities/<int:id>', methods=['DELETE'])
def delete_liability(id):
    liability = Liability.query.get(id)
    if liability:
        db.session.delete(liability)
        db.session.commit()
        return jsonify({'message': 'Liability deleted successfully'}), 200
    else:
        return jsonify({'message': 'Liability not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
