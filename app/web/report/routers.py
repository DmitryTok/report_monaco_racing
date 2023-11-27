from flask import Blueprint, Response, render_template

from app.utils.queries import get_driver, get_drivers, get_result

report_router = Blueprint('routers', __name__)


@report_router.route('/', methods=['GET'])
def index() -> Response:
    return Response(render_template('index.html'))


@report_router.route('/report', methods=['GET'])
def report() -> Response:
    result = get_result()
    return Response(render_template('report.html', report=result))


@report_router.route('/drivers', methods=['GET'])
def all_drivers() -> Response:
    drivers = get_drivers()
    return Response(render_template('drivers.html', drivers=drivers))


@report_router.route('/driver/<string:abbr>', methods=['GET'])
def driver_info(abbr: str) -> Response:
    driver = get_driver(abbr)
    if driver is None:
        return Response(
            response={f'Driver with abbr {abbr}, not exists'},
            content_type='application/json',
            status=404,
        )
    return Response(render_template('driver_info.html', driver=driver))
