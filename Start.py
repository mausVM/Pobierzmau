from flask import Flask, render_template, session, redirect, url_for, send_from_directory, request, flash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

USERS = {
    "Mau": "Maus",
    "Gumiś": "Kartofel"
}


# Logowanie
@app.route("/", methods=["GET", "POST"])
def login():
    from flask import request, flash
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username] == password:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Nieprawidłowy login lub hasło")
    return render_template("login.html")

# Strona główna
@app.route("/index")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    # Pobieranie listy plików w downloads
    files = []
    if os.path.exists(DOWNLOAD_DIR):
        files = [f for f in os.listdir(DOWNLOAD_DIR) if os.path.isfile(os.path.join(DOWNLOAD_DIR, f))]
    return render_template("index.html", username=session["username"], files=files)

# Pobieranie plików
@app.route("/download/<filename>")
def download(filename):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

# Wylogowanie
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
