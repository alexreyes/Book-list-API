from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def hello(): 
    return jsonify({"about": "Hello World!"})

@app.route("/bookList")
def bookList(): 
    file = open('bookList.txt', 'r')
    lines = file.read().split("\n")
    return jsonify(lines)
    # return jsonify([{"Title": "Supermarket", "Author": "Bobby Hall"}])

if __name__ == '__main__':
    app.run(debut=True)