from flask import Flask
from flask import render_template
from flask import request
from flask import redirect


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/submit", methods=["POST", "GET"])
def submit():
    name = request.form.get("name", None)
    gender = request.form.get("gender", None)
    thing = request.form.get("thing", None)

    error = None

    if name is None or name == "":
        error = "Name is required"
    elif gender is None or gender == "":
        error = "Gender is required"
    elif thing is None or thing == "":
        error = "Thing is required"

    if error is not None:
        return render_template("index.html", error=error)

    with open("signups.txt", "a") as f:
        f.write(
            "{name},{gender},{thing}\n".format(
                name=name,
                gender=gender,
                thing=thing,
            )
        )

    return redirect("/success")
