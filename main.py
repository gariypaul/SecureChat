from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"
socketio = SocketIO(app)

#mock database
data = {"Bob": "1234", "Alice": "1234"}
rooms = {}


#TODO: add a routes
@app.route("/", methods=["GET", "POST"])
def login():
    #TODO: Edit post request to add encryption 
    if request.method == "POST":
        name = request.form["name"]
        password  = request.form["password"]
        session["name"] = name

        if not name:
            return render_template("login.html", error="Invalid name")
        if not password:
            return render_template("login.html", error="Invalid password")

        if authenticate(name, password):
            return redirect(url_for("start_chat"))
        else:
            return render_template("login.html", error="Invalid credentials")
        
    return render_template("login.html")

@app.route("/start_chat", methods=["GET", "POST"])
def start_chat():
    if request.method == "POST":
        user_a = session["name"]
        user_b = request.form["user_b"]
        session["user_b"] = user_b

        #generate a unique chat id using sha256 hash using user_a and user_b names
        chat_id = hashlib.sha256(f"{user_a}{user_b}".encode()).hexdigest()
        return redirect(url_for("chat", chat_id=chat_id))
    return render_template("start_chat.html", users = data.keys(), current_user=session["name"])

@app.route("/chat/<chat_id>", methods=["GET", "POST"])
def chat(chat_id):
    if chat_id not in rooms:
        rooms[chat_id] = []
  
        
    
    return render_template("chat.html", chat_id=chat_id, messages=rooms[chat_id],users = data.keys(),current_user=session["name"], user_b=session["user_b"])

#TODO: add socketIO event handlers\
@socketio.on("join")
def handle_join(data):
    chat_id = data["chat_id"]
    join_room(chat_id)
    
    

@socketio.on("send_message")
def handle_send_message(data):
    chat_id = data["chat_id"]
    user_a = session["name"]
    if chat_id not in rooms:
        rooms[chat_id] = []
    message = data["message"]
    rooms[chat_id].append([user_a, message])
    emit('message', {"user": user_a, "message": message}, room=chat_id)


def authenticate(name, password):
    if name in data:
        return data[name] == password
    return False

if __name__ == "__main__":
    socketio.run(app)   #run the app


