from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html",
                           title="Home")


@app.route('/<math>/<int:num1>/<int:num2>')
@app.route('/<math>/<float:num1>/<float:num2>')
@app.route('/<math>/<int:num1>/<float:num2>')
@app.route('/<math>/<float:num1>/<int:num2>')
def math(num1, num2, math):
    if math == "add":
        answer = num1 + num2
        symbol = '+'
    if math == "sub":
        answer = num1 - num2
        symbol = '-'
    if math == "mul":
        answer = num1 * num2
        symbol = '*'
    if math == "div":
        answer = num1 / num2
        symbol = '/'
    context = {'num1': num1, 'num2': num2, 'answer': answer, 'symbol': symbol}
    return render_template("math.html", **context)


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
