import os
import threading
from flask import Flask, jsonify, request
import settings

app = Flask(__name__)

USER_ID = {}


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_vk_id(username):
    if username in USER_ID.keys():
        vk_id = USER_ID[username]
        return {'vk_id': vk_id}, 200
    else:
        return jsonify({}), 404


@app.route('/vk_id/<username>', methods=['POST'])
def add_user_vk_id(username):
    if username in USER_ID.keys():
        return jsonify('ID already exists'), 400
    else:
        USER_ID[username] = request.json['vk_id']
        return jsonify("Successful"), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })

    server.start()
    return server


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


if __name__ == '__main__':
    host, port = os.environ.get('VK_URL', '127.0.0.1:5000').split(":")
    app.run(host, port)
    # app.run(host=settings.MOCK_HOST, port=settings.MOCK_PORT)
