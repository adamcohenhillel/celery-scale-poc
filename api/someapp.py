"""
Example of how to use Celery within Flask's views
(trigger tasks and read tasks' results)
"""
from flask import Blueprint, jsonify, current_app


someapp_bp = Blueprint('someapp_bp', __name__)


@someapp_bp.route('/tasks', methods=['POST'])
def longtask():
    """Create new task"""
    task = current_app.celery.send_task('long_task')
    return jsonify(task_id=task.id), 202


@someapp_bp.route('/tasks/<task_id>')
def taskstatus(task_id):
    task = current_app.celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
