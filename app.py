from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return "Hello, World!"


@app.route("/", methods=['POST'])
def disp_chart():
    return "Disp Chart!"

if __name__ == "__main__":
    app.run()