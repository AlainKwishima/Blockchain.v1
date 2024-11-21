from flask import Flask, jsonify, request
from flask_cors import CORS
import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Serialize the block data into a string and hash it
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, latest_block.hash)
        self.chain.append(new_block)
        return new_block

# Initialize Flask app and Blockchain
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify([block.__dict__ for block in blockchain.chain]), 200

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json.get('data', '')
    if not data:
        return jsonify({'error': 'Data is required'}), 400
    new_block = blockchain.add_block(data)
    return jsonify(new_block.__dict__), 201

if __name__ == '__main__':
    app.run(debug=True)
