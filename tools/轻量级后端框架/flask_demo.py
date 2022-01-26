from tools import exec_ssh_command
from flask import Flask, request
from mysql import Delete
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def index():
    return 'hello world'


@app.route('/command', methods=['GET', 'POST'])
def exec_command():
    command = request.json.get("command")
    res = exec_ssh_command(command)
    return res


@app.route('/delete_user', methods=['GET'])
def delete_user():
    user_phone = request.args.get("user_phone")
    ops = Delete(user_phone)
    try:
        ops.func_list()
        return f"{user_phone}-删除成功了！"
    except Exception as e:
        return f"str({e})"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)