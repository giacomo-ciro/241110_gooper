from flask import Flask, request, jsonify
from gooper import GooperModel

gooper = GooperModel()
app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
