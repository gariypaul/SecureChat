from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
import hashlib
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
import base64


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"
socketio = SocketIO(app)

#mock database
users = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry", "Isabella", "Jack", "Kate", "Liam", "Mia", "Noah", "Olivia", "Peter", "Queen", "Rose", "Sam", "Tom", "Umar", "Victor", "Wendy", "Xander", "Yvonne", "Zara"]
rooms = {}

#key derivation function
def derive_key(password: str, salt: bytes, iterations: int = 100000, key_size: int = 32):
    return PBKDF2(password, salt, dkLen=key_size, count=iterations, hmac_hash_module=SHA256)

def encrypt_message(key,plaintext):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plaintext.encode(),AES.block_size))
    return base64.b64encode(iv + cipher_text).decode('utf-8')




#TODO: add a routes
@app.route("/", methods=["GET", "POST"])
def login():
    #TODO: Edit post request to add encryption 
    if request.method == "POST":
        name = request.form["name"]
        if name not in users:
            users.append(name)
        session["password"] = request.form["password"]
        session["name"] = name

        if not name:
            return render_template("login.html", error="Invalid name")
        return redirect(url_for("start_chat"))
        
    return render_template("login.html")

@app.route("/start_chat", methods=["GET", "POST"])
def start_chat():
    if request.method == "POST":
        user_a = session["name"]
        user_b = request.form["user_b"]
        session["user_b"] = user_b

        #generate a unique chat id using sha256 hash using user_a and user_b names
        chat_id = generate_chat_id(user_a, user_b)
        return redirect(url_for("chat", chat_id=chat_id))
    return render_template("start_chat.html", users = users, current_user=session["name"])

@app.route("/chat/<chat_id>", methods=["GET", "POST"])
def chat(chat_id):
    if chat_id not in rooms:
        rooms[chat_id] = []
  
        
    
    return render_template("chat.html", chat_id=chat_id, messages=rooms[chat_id],users = users,current_user=session["name"], user_b=session["user_b"])

#TODO: add socketIO event handlers\
@socketio.on("join")
def handle_join(data):
    chat_id = data["chat_id"]
    join_room(chat_id)
    
    

@socketio.on("send_message")
def handle_send_message(data):
    chat_id = data["chat_id"]
    user_a = session["name"]
    password = session["password"]
    if chat_id not in rooms:
        rooms[chat_id] = []
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    print("Derived key: ", key.hex())

    encrypted_message = encrypt_message(key, data["message"])
    encoded_salt = base64.b64encode(salt).decode('utf-8')
    rooms[chat_id].append([user_a, encrypted_message, encoded_salt])
    emit('message', {"user": user_a, "message": encrypted_message, "salt":encoded_salt}, room=chat_id)

def generate_chat_id(user_a, user_b):
    user_a_cleaned = user_a.strip().lower()
    user_b_cleaned = user_b.strip().lower()
    sorted_users = sorted([user_a_cleaned, user_b_cleaned])
    chat_id = hashlib.sha256(f"{sorted_users[0]}{sorted_users[1]}".encode()).hexdigest()
    return chat_id


if __name__ == "__main__":
    socketio.run(app)   #run the app


