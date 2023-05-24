from flask import Flask, Response, request, make_response
from threading import RLock, Thread
from game.update import Update
from http import HTTPStatus
import string
from random import choice
import json

ADMIN_PASSWORD = "neilscottzack"
NUM_PLAYERS = 2

# Creates a 4-letter long alphanumeric password
def create_password():
    pw = ""
    for _ in range(5):
        pw += choice(string.digits)
    return pw

def do_webserve(updates: list, updates_lock: RLock):
    app = Flask(__name__) 

    # The list of passwords for the players.
    # The admin is always player 0, and player-n has their password at passwords[n]
    passwords: list[str] = [ADMIN_PASSWORD] + [create_password() for _ in range(NUM_PLAYERS)]

    # Update all of the non-admin passwords
    def update_passwords():
        nonlocal passwords

        for i in range(NUM_PLAYERS):
            # Offset by 1 because the admin password is at index 0
            passwords[i + 1] = create_password()

    def get_player_from_pw(pw: str):
        nonlocal passwords

        if pw not in passwords:
            return -1
        
        return passwords.index(pw)
 
    # Look ma, no flask_cors!
    def after_request(r: Response):
        r.access_control_allow_origin = "*"
        return r
    app.after_request(after_request)

    def do_welcome():
        return "Welcome to webserve!"

    def user_check_password():
        try:
            data = json.loads(request.get_data())
        except:
            return Response(status=HTTPStatus.BAD_REQUEST)

        if "authToken" not in data:
            return Response("authToken must be provided", status=HTTPStatus.BAD_REQUEST)
        
        player_index = get_player_from_pw(data['authToken'])
        if player_index >= 0:
            return Response(json.dumps({'playerIndex': player_index}), status=HTTPStatus.OK)
        else:
            return Response(status=HTTPStatus.UNAUTHORIZED)

    def user_send_control():
        try:
            data = json.loads(request.get_data())
        except:
            return Response(status=HTTPStatus.BAD_REQUEST)

        if "authToken" not in data:
            return Response("authToken must be provided", status=HTTPStatus.BAD_REQUEST)
        if "button" not in data:
            return Response("button must be provided", status=HTTPStatus.BAD_REQUEST)

        # Validate that they're authenticated
        auth_token = data['authToken']
        print("token is " + auth_token)

        player_index = get_player_from_pw(auth_token)
        if player_index < 0:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        
        button = data['button']

        if type(button) != int:
            return Response("button must be an integer", status=HTTPStatus.BAD_REQUEST)
        if not Update.is_button_valid(int(button)):
            return Response(f"button index {button} was invalid", status=HTTPStatus.BAD_REQUEST)

        updates_lock.acquire()
        updates.append(Update(button=button, player_index=player_index))
        updates_lock.release()

        return Response(status=HTTPStatus.OK)
    
    def admin_rotate_passwords():
        try:
            data = json.loads(request.get_data())
        except:
            return Response(status=HTTPStatus.BAD_REQUEST)

        if 'authToken' not in data:
            return Response("authToken must be provided", status=HTTPStatus.BAD_REQUEST)

        player_index = get_player_from_pw(data['authToken'])            
        if player_index != 0:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        
        update_passwords()
        return Response(json.dumps({"authTokens": passwords[1:]}), status=HTTPStatus.OK)
    
    def admin_get_passwords():
        try:
            data = json.loads(request.get_data())
        except:
            return Response(status=HTTPStatus.BAD_REQUEST)

        if 'authToken' not in data:
            return Response("authToken must be provided", status=HTTPStatus.BAD_REQUEST)

        player_index = get_player_from_pw(data['authToken'])            
        if player_index != 0:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        
        return Response(json.dumps({"authTokens": passwords[1:]}), status=HTTPStatus.OK)
        
    
    app.add_url_rule("/", "do_welcome", do_welcome)

    # ===========================
    # PLAYER-FACING ROUTES
    # ===========================
    app.add_url_rule("/user/password", "user_check_password", user_check_password, methods=["POST"])
    app.add_url_rule("/user/control", "user_send_control", user_send_control, methods=["POST"])
    
    # ===========================
    # ADMIN ROUTES
    # ===========================
    app.add_url_rule("/admin/passwords", "admin_get_passwords", admin_get_passwords, methods=["POST"])
    app.add_url_rule("/admin/rotate", "admin_rotate_passwords", admin_rotate_passwords, methods=["POST"])

    app.run(port=8160)
