import celery.states as states
from flask import Flask, Response
from flask import url_for, jsonify
from worker import celery

dev_mode = True
app = Flask(__name__)


@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    return f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"


@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    return res.state if res.state == states.PENDING else str(res.result)


@app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
