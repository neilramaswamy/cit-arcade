from flask import Flask, Response, request, make_response
from threading import RLock
from game.update import Update
import json

def do_webserve(updates: list, updates_lock: RLock):
    app = Flask(__name__) 

    # Look ma, no flask_cors!
    def after_request(r: Response):
        r.access_control_allow_origin = "*"
        return r
    app.after_request(after_request)

    def do_welcome():
        return "Welcome to webserve!"

    def do_nes():
        response = make_response()

        try:
            data = json.loads(request.get_data())

            if not data['button']:
                raise AttributeError()

            button = data['button']
            print(button, type(button))

            if type(button) != int:
                raise TypeError()

            updates_lock.acquire()
            updates.append(Update(button))
            updates_lock.release()

            response.status_code = 200
            response.data = "Success"
        except AttributeError:
            response.status_code = 400
            response.data = "No update property found"
        except TypeError:
            response.status_code = 400
            response.data = "Update property of wrong type"
        except ValueError:
            response.status_code = 400
            response.data = "Update property is wrong value (expected [1, 8])"
        except:
            response.status_code = 400
            response.data = "Invalid request"

        return response

    app.add_url_rule("/", "do_welcome", do_welcome)
    app.add_url_rule("/nes", "do_nes", do_nes, methods=["POST"])

    app.run(port=8160)