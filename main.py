from flask import Flask
from celery import Celery

from config import WorkerConfig
from api.someapp import someapp_bp


def make_celery(app=None):
    app = app or create_flask_app()
    celery = Celery(
        'worker555',
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        include=['tasks']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_flask_app():
    app = Flask(__name__)
    app.config.from_object(WorkerConfig)
    app.register_blueprint(someapp_bp)
    app.celery = make_celery(app)
    return app


# # Send two numbers to add
# @app.route('/add/<int:param1>/<int:param2>')
# def add(param1,param2):  
#     task = celery.send_task('mytasks.add', args=[param1, param2])
#     return task.id

# # Check the status of the task with the id found in the add function
# @app.route('/check/<string:id>')
# def check_task(id):  
#     res = celery.AsyncResult(id)
#     return res.state if res.state==states.PENDING else str(res.result)


if __name__ == "__main__":
    app = create_flask_app()
    app.run(host='0.0.0.0', debug=True)