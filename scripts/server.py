import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration
VAULT_ROOT = '/storage/emulated/0/Download/Vinci'
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large" # Example model, can be changed
# IMPORTANT: Set your Hugging Face Token as an environment variable 'HF_API_TOKEN'
# or replace "YOUR_HF_TOKEN_HERE" below.
HF_API_TOKEN = os.environ.get("HF_API_TOKEN", "YOUR_HF_TOKEN_HERE")

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

@app.route('/')
def home():
    return "Obsidian AI Server is running!"

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({"error": "No path provided"}), 400
    
    full_path = os.path.join(VAULT_ROOT, file_path)
    
    # Security check to prevent reading outside vault
    if not os.path.abspath(full_path).startswith(VAULT_ROOT):
         return jsonify({"error": "Access denied"}), 403

    if not os.path.exists(full_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/write', methods=['POST'])
def write_file():
    data = request.json
    file_path = data.get('path')
    content = data.get('content')
    
    if not file_path or content is None:
        return jsonify({"error": "Path or content missing"}), 400

    full_path = os.path.join(VAULT_ROOT, file_path)

    # Security check
    if not os.path.abspath(full_path).startswith(VAULT_ROOT):
         return jsonify({"error": "Access denied"}), 403

    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({"message": "File written successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    payload = {"inputs": prompt}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"Server starting on port 5000...")
    print(f"Vault Root: {VAULT_ROOT}")
    app.run(host='0.0.0.0', port=5000, debug=True)
