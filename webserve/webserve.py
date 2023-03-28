from flask import Flask, Response
from threading import RLock
from game.update import Update

def do_webserve(updates: list, updates_lock: RLock):
    app = Flask(__name__) 

    # Look ma, no flask_cors!
    def after_request(r: Response):
        r.access_control_allow_origin = "*"
        return r
    app.after_request(after_request)

    def do_up():
        print("Recevied UP command")

        updates_lock.acquire()
        updates.append(Update(dy = -1))
        updates_lock.release()

        return "up"
    
    def do_down():
        print("Recevied DOWN command")

        updates_lock.acquire()
        updates.append(Update(dy = 1))
        updates_lock.release()

        return "down"

    def do_right():
        print("Recevied RIGHT command")

        updates_lock.acquire()
        updates.append(Update(dx = 1))
        updates_lock.release()

        return "right"
    
    def do_left():
        print("Recevied LEFT command")

        updates_lock.acquire()
        updates.append(Update(dx = -1))
        updates_lock.release()

        return "left"


    app.add_url_rule("/up", "do_up", do_up)
    app.add_url_rule("/down", "do_down", do_down)
    app.add_url_rule("/right", "do_right", do_right)
    app.add_url_rule("/left", "do_left", do_left)

    app.run(port=8160)