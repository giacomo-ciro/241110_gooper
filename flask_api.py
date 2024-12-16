from flask import Flask
from gooper import GooperModel

gooper = GooperModel()
app = Flask(__name__)
docs = "Welcome to the Gooper API. The only available endpoint is `/generate/` followed by the user's prompt the model will respond to. For example, '/generate/my%20brand%20specializes%20in%20food' will generate a response to the prompt 'my brand specializes in food'"
@app.route('/')
def hello_world():
    return docs
    
@app.route('/generate/<string:prompt>')
def generate(prompt):
    response = gooper.generate(prompt)
    return {"response": response}

if __name__ == '__main__':
    app.run(debug=True)
