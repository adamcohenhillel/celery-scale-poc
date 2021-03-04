from flask import Flask
from celery import Celery

from .config import Config, Config2
from .api import api_bp


def create_celery_app(app=None):
    app = app or create_flask_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
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
    app.config.from_object(Config)
    app.register_blueprint()
    return app


if __name__ == '__main__':
    app = create_flask_app()
    app.run(debug=True, host='0.0.0.0')