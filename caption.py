from flask import Flask, render_template, request
import pycaption

app = Flask(__name__)

@app.route("/test", methods=["POST"])
def test():
    return _test(request.form["test"])

@app.route("/index")
def index():
    return _test("My Test Data")

@app.route("/")
def home():
	return "Hello"

def _test(argument):
    return None


if __name__ == '__main__':
    app.run(debug=True)