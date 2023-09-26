from flask import Flask
from flask import request as r
from flask_cors import CORS, cross_origin
import sqlite3
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_user_info(uid):
    db = sqlite3.connect('heylon_api_sqlite3.sqlite3')
    sql = db.cursor()
    user_info = {'uid': uid}

    sql.execute(f"SELECT uid FROM users WHERE uid = {uid}")
    if sql.fetchone() is None:
        user_info['on_server'] = "false"
        user_info['server_nick'] = "no"
        user_info['role'] = "no"
    else:
        for on_server in sql.execute(f"SELECT on_server FROM users WHERE uid = {uid}"):
            on_server = on_server[0]
        user_info['on_server'] = on_server
        for server_nick in sql.execute(f"SELECT server_nick FROM users WHERE uid = {uid}"):
            server_nick = server_nick[0]
        user_info['server_nick'] = server_nick
        for role in sql.execute(f"SELECT role FROM users WHERE uid = {uid}"):
            role = role[0]
        user_info['role'] = role
    return user_info

@cross_origin()
@app.route('/api/check', methods=['GET'])
def save():
    try:
        uid = r.args.get("uid")
        if uid:
            try:
                uid = int(uid)
            except ValueError:
                return 'uid must be integer'
            user_info = get_user_info(uid)
            return user_info
        else:
            return 'no "uid" param was given'
    except Exception as e:
        print(e)
        return 'error'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8892, debug=True)