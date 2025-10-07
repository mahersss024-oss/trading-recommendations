"""
Trading Recommendations API
A simple Flask-based API for trading recommendations
"""

from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# Sample trading recommendations data
recommendations = [
    {
        "id": 1,
        "symbol": "AAPL",
        "action": "BUY",
        "price": 175.50,
        "target": 185.00,
        "stop_loss": 170.00,
        "timestamp": datetime.now().isoformat()
    },
    {
        "id": 2,
        "symbol": "GOOGL",
        "action": "HOLD",
        "price": 140.25,
        "target": 150.00,
        "stop_loss": 135.00,
        "timestamp": datetime.now().isoformat()
    }
]

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to Trading Recommendations API",
        "version": "1.0.0",
        "endpoints": {
            "/": "This help message",
            "/health": "Health check endpoint",
            "/api/recommendations": "Get all trading recommendations",
            "/api/recommendations/<id>": "Get a specific recommendation"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get all trading recommendations"""
    return jsonify({
        "success": True,
        "count": len(recommendations),
        "data": recommendations
    })

@app.route('/api/recommendations/<int:rec_id>', methods=['GET'])
def get_recommendation(rec_id):
    """Get a specific recommendation by ID"""
    rec = next((r for r in recommendations if r['id'] == rec_id), None)
    if rec:
        return jsonify({
            "success": True,
            "data": rec
        })
    return jsonify({
        "success": False,
        "error": "Recommendation not found"
    }), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
