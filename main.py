from flask import Flask

from api.someapp import someapp_bp
from worker import celery as celery_w


def create_app():
    app = Flask(__name__)
    celery.conf.update(app.config)
    app.celery = celery_w
    app.register_blueprint(someapp_bp)
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
