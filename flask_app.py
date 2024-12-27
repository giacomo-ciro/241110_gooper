from flask import Flask, request, jsonify
from gooper import GooperModel
from flask_cors import CORS

# import os
# os.chdir('./mysite')

gooper = GooperModel()
app = Flask(__name__)
CORS(app)

# gooper = GooperModel(model_text="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")    # 0.18$
gooper = GooperModel(model_text="meta-llama/Meta-Llama-3-8B-Instruct-Lite")         # 0.10$

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

@app.route('/influencer_count', methods=['GET'])
def influencer_count():
    return jsonify({"response": gooper.get_influencer_count()})

@app.route('/model_name', methods=['GET'])
def model_name():
    return jsonify({"response": gooper.model_text})

if __name__ == '__main__':
    app.run(debug=True)
