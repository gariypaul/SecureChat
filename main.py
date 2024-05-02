from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
import hashlib

app = Flask(__name__, static_folder="/")
app.config["SECRET_KEY"] = "mysecret"
socketio = SocketIO(app)

#mock database
data = {}

#TODO: add a routes
@app.route("/", methods=["GET", "POST"])
def login():
    #TODO: Edit post request to add encryption 
    if request.method == "POST":
        name = request.form["name"]
        password  = request.form["password"]
        session["name"] = name
        return redirect(url_for("chat"))

        if not username:
            return render_template("index.html", error="Invalid name")
        if not password:
            return render_template("index.html", error="Invalid password")

    return render_template("login.html")

@app.route("/start_chat", methods=["GET", "POST"])
def start_chat():
    if request.method == "POST":
        user_a = request.form["user_a"]
        user_b = request.form["user_b"]

        #generate a unique chat id using sha256 hash using user_a and user_b names
        chat_id = hashlib.sha256(f"{user_a}{user_b}".encode()).hexdigest()
        return redirect(url_for("chat", chat_id=chat_id))
    return render_template("start_chat.html")

@app.route("/chat/<chat_id>")
def chat(chat_id):
    return render_template("chat.html", chat_id=chat_id)

#TODO: add socketIO event handlers


if __name__ == "__main__":
    socketio.run(app)   #run the app


