from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send
app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")
connected_clients = {}
@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print("Client connected")
    connected_clients[request.sid] = {"username": "Anonymous"}
    send("Welcome to the Chat Labs!")

@socketio.on('disconnect')
def disconnect():
    print("Client disconnected")
    if request.sid in connected_clients:
        username = connected_clients[request.sid]["username"]
        send(f"{username} has left the chat!", broadcast=True)
        del connected_clients[request.sid]

@socketio.on('message')
def handle_message(msg, data=None):
    print(f"Received message: {msg}, data: {data}")
    if data and "username" in data and "socketId" in data:
        connected_clients[data["socketId"]] = {"username": data["username"]}
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)