
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import json
from datetime import datetime
import random

app = Flask(__name__)
Bootstrap(app)

# Simulated transaction database with more realistic data
TRANSACTION_DB = {
    "TXN123456": {
        "status": "completed",
        "amount": 1200.50,
        "timestamp": "2024-04-24 10:30:15",
        "merchant": "Amazon India",
        "features": {"velocity": 0.2, "amount_ratio": 0.3, "merchant_risk": 0.1}
    },
    "TXN987654": {
        "status": "failed",
        "amount": 800.00,
        "timestamp": "2024-04-24 11:45:30",
        "merchant": "Flipkart",
        "error": "Insufficient funds"
    },
    "TXN456789": {
        "status": "pending",
        "amount": 2500.00,
        "timestamp": "2024-04-24 12:15:45",
        "merchant": "Swiggy"
    }
}

def predict_fraud(transaction):
    """Simple rule-based fraud prediction"""
    features = transaction.get('features', {})
    risk_score = (
        features.get('velocity', 0) * 0.4 +
        features.get('amount_ratio', 0) * 0.3 +
        features.get('merchant_risk', 0) * 0.3
    )
    return (1 if risk_score > 0.5 else 0, risk_score)

@app.route('/api/transaction/<txn_id>')
def api_get_transaction(txn_id):
    transaction = TRANSACTION_DB.get(txn_id)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(transaction)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        # Enhanced fraud detection logic
        features = {
            "velocity": random.uniform(0, 1),
            "amount_ratio": 0.8 if amount > 10000 else 0.2,
            "merchant_risk": random.uniform(0, 0.5)
        }
        prediction, probability = predict_fraud({"features": features})
        return render_template('prediction.html', 
                             prediction=prediction, 
                             probability=probability,
                             amount=amount)
    return render_template('predict.html')

@app.route('/check_transaction', methods=['GET', 'POST'])
def check_transaction():
    if request.method == 'POST':
        txn_id = request.form['transaction_id']
        transaction = TRANSACTION_DB.get(txn_id)
        
        if transaction:
            status = transaction['status']
            
            # For completed transactions, perform enhanced fraud check
            if status == 'completed':
                prediction, probability = predict_fraud(transaction)
            else:
                prediction = None
                probability = None
                
            return render_template('transaction_status.html', 
                                 transaction_id=txn_id,
                                 transaction=transaction,
                                 prediction=prediction,
                                 probability=probability)
        else:
            return render_template('transaction_status.html', 
                                 transaction_id=txn_id,
                                 error="Transaction not found")
            
    return render_template('check_transaction.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
