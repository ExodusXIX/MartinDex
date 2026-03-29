from flask import Flask, render_template, jsonify, request
from parser import search, get_all

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pokemon/<query>')
def pokemon(query):
    result = search(query)
    if result:
        return jsonify(result)
    return jsonify({'error': 'Pokemon not found'}), 404

@app.route('/api/all')
def all_pokemon():
    return jsonify(get_all())

if __name__ == '__main__':
    app.run(debug=True)
