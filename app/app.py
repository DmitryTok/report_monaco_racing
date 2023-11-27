import atexit
from typing import Any

from flask import Flask
from flask_restful import Api

from app.api.api_report import APIDriver, APIDrivers, APIReport
from app.constants import RUN_DEBUG, RUN_HOST, RUN_PORT
from app.db.session import close_dbs, pop_session, set_session
from app.logger import logger_config
from app.web.report.routers import report_router


def create_app() -> Flask:
    logger_config()

    app = Flask(__name__, template_folder='web/templates')
    api = Api(app)

    app.before_request(set_session)

    @app.teardown_request
    def handle_session(args) -> Any:
        pop_session()
        return args

    app.register_blueprint(report_router)

    api.add_resource(APIReport, '/api/report/')
    api.add_resource(APIDrivers, '/api/drivers/')
    api.add_resource(APIDriver, '/api/driver/<abbr>')
    return app


app = create_app()


if __name__ == '__main__':
    atexit.register(close_dbs)
    app.run(host=RUN_HOST, port=int(RUN_PORT), debug=bool(RUN_DEBUG))
