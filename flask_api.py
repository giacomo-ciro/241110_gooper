from flask import Flask, request, jsonify
from gooper import GooperModel
from flask_cors import CORS

gooper = GooperModel()
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return open("api_docs.html", "r").read()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Invalid input, "prompt" is required'}), 400
    
    prompt = data['prompt']
    response = gooper.generate(prompt)
    
    return jsonify({"response": response})

@app.route('/model_version', methods=['GET'])
def version():
    return jsonify({"response": gooper.version})

@app.route('/database_count', methods=['GET'])
def database_count():
    return jsonify({"response": gooper.get_influencer_count()})

if __name__ == '__main__':
    app.run(debug=True)
