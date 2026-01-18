from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.orchestrator import OrchestratorAgent
import os

app = Flask(__name__)
CORS(app)

# Initialize Orchestrator (loads models, might take a few seconds)
orchestrator = OrchestratorAgent()

@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({"status": "active", "system": "Preventive Care Agentic AI"})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        user_data = data.get('user_data')
        history = data.get('history', [])
        
        if not user_data:
            return jsonify({"error": "No user_data provided"}), 400
            
        result = orchestrator.process_request(user_data, history)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
