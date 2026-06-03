from flask import Flask, render_template, request, redirect, session
import pickle

app = Flask(__name__)
app.secret_key = "secret123"

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

USERNAME = "admin"
PASSWORD = "1234"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == USERNAME and password == PASSWORD:
        session["user"] = username
        return redirect("/home")

    return render_template(
        "login.html",
        error="Invalid Credentials"
    )

@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/")

    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect("/")

    message = request.form["message"]

    data = vectorizer.transform([message])

    prediction = model.predict(data)[0]

    if prediction == 1:
        result = "Spam"
        confidence = 95
    else:
        result = "Not Spam"
        confidence = 92

    return render_template(
        "index.html",
        result=result,
        confidence=confidence
    )

@app.route("/logout")
def logout():

    session.pop("user",None)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)