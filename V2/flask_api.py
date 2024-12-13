from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask 2.0!'
    
@app.route('/wordcount/<string:prompt>')
def word_count(prompt):
    n = len(prompt.split(' '))
    return {"length": n}

if __name__ == '__main__':
    app.run(debug=True)
