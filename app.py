"""
Created on Sun May  4 11:43:41 2025

@author: Kittisci
"""

from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Store slot map in memory (for now)
system_map = []

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/colPlanner')
def colPlanner():
    return render_template('colPlanner.html')

@app.route('/add_body', methods=['POST'])
def add_body():
    data = request.get_json()
    body_name = data['body']
    surface_slots = int(data['surface'])
    orbital_slots = int(data['orbital'])

    slots = []
    for i in range(surface_slots):
        slots.append({
            "SlotID": f"{body_name}-Surface-{i+1}",
            "Body": body_name,
            "Type": "Surface",
            "Filled": False
        })
    for i in range(orbital_slots):
        slots.append({
            "SlotID": f"{body_name}-Orbital-{i+1}",
            "Body": body_name,
            "Type": "Orbital",
            "Filled": False
        })

    system_map.extend(slots)
    return jsonify({"message": "Body added", "slots": system_map})

@app.route('/get_map')
def get_map():
    return jsonify(system_map)

@app.route('/save', methods=['POST'])
def save_map():
    with open('system_map.json', 'w') as f:
        json.dump(system_map, f, indent=2)
    return jsonify({"message": "System map saved"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)