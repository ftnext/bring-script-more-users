import random

from flask import Flask, render_template


NUMBERS = list(range(10))
app = Flask(__name__)


def say_hello():
    return f"Hello World {random.choice(NUMBERS)}"


@app.route("/hello")
def hello():
    message = say_hello()
    return render_template("hello.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
