import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session
import json
from channels import Channel
from messages import Message
from user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"
SESSION_TYPE = 'filesystem'
socketio = SocketIO(app)
Session(app)

channels = []
users = []

channels.append(Channel(index=0, name="First"))
channels.append(Channel(index=1, name="Second"))

channels[0].add_message(Message(User("", "Admin", 0), "Test"))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", channels=channels)
    else:
        u_name = request.form.get("nickname")
        u_channel = int(request.form.get("channel"))
        new_user = User(request.args.get("t"), u_name, u_channel)
        if new_user in users:
            flash("User with that name is already logged")
            return redirect("/", "303")
        session["user"] = u_name
        session["channel"] = u_channel
        return redirect("/channel")


@app.route("/channel")
def channel():
    if session.get("user"):
        u_name = session["user"]
        u_channel = session["channel"]
        return render_template("channel.html", channel=channels[u_channel], user=u_name, prev_user="None")
    else:
        flash("You are not logged")
        return redirect("/", "303")


@app.route("/channels", methods={"GET"})
def channels_view():
    if request.method == "GET":
        if session.get("user"):
            u_name = session["user"]
            if request.args.get("ch"):
                new_channel = int(request.args.get("ch"))
                session["channel"] = new_channel
                return redirect("/channel")
            else:
                return render_template("channels.html", channels=channels, user=u_name)
        else:
            flash("You are not logged")
            return redirect("/", "303")


@app.route("/create_channel", methods=["GET", "POST"])
def create_channel():
    if request.method == "GET":
        return render_template("create_channel.html")
    else:
        new_channel_name = request.form.get("channel_name")
        new_channel = Channel(index=len(channels), name=new_channel_name)
        channels.append(new_channel)
        flash("Channel created successfully")
        return redirect("/channels")


@socketio.on("register_on_channel")
def select_channel(data):
    u_name = data["nickname"]
    u_channel = int(data["channel"])
    new_user = User(request.args.get("t"), u_name, u_channel)
    print(request.args.get("t"), u_name, u_channel)
    join_room(u_channel)
    users.append(new_user)
    channels[u_channel].users.append(u_name)
    nickname_array = json.dumps(channels[u_channel].users)
    print(nickname_array)
    emit("current_client_list", {"users": nickname_array}, room=u_channel)


@socketio.on("new_message")
def new_message(data):
    u_name = data["nickname"]
    u_channel = int(data["channel"])
    user = User(request.args.get("t"), u_name, u_channel)
    print(request.args.get("t"), u_name, u_channel)
    if user in users:
        join_room(u_channel)
        text = data["message"]
        msg = Message(user, text)
        channels[u_channel].add_message(msg)
        print("receivde msg:", text, "from", u_name)
        emit("write_message", {
            "nickname": u_name,
            "message": text
        }, room=u_channel)
    else:
        print("user not found", u_name, u_channel)
        for user in users:
            print(user.id, user.name, user.channel)


@socketio.on('connect')
def connect():
    print("Client connected", request.args.get("t"))


@socketio.on('disconnect')
def disconnect():
    print("Client disconnected", request.args.get("t"))
    del_user = User(request.args.get("t"), "", 0)
    index = users.index(del_user)
    user = users[index]
    channels[user.channel].users.remove(user.name)
    nickname_array = json.dumps(channels[user.channel].users)
    print(nickname_array)
    emit("current_client_list", {"users": nickname_array}, room=user.channel)
    users.remove(user)

