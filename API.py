from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello(): 
    return jsonify({"about": "Hello World!"})

@app.route("/bookList")
def bookList(): 
    file = open('bookList.txt', 'r')
    lines = file.read().split("\n")
    
    response = jsonify(lines)
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    file.close()
    
    return response