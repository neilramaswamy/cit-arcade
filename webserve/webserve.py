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
        updates_lock.acquire()
        updates.append(Update(dy = -1))
        updates_lock.release()

        return "up"
    
    def do_down():
        updates_lock.acquire()
        updates.append(Update(dy = 1))
        updates_lock.release()

        return "down"

    app.add_url_rule("/up", "do_up", do_up)
    app.add_url_rule("/down", "do_down", do_down)

    app.run(port=8160)