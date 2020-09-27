from flask import Flask, render_template


app = Flask(__name__)


@app.route("/integration")
def integration():
    return render_template("integration.html")


if __name__ == "__main__":
    app.run(debug=True)
