from typing import Any

from flask import Response
from flask_restful import Resource

from app.utils.queries import (
    get_driver,
    get_drivers,
    get_result,
    result_as_dict
    )


class APIReport(Resource):
    def get(self) -> dict[str, list[dict[str, Any]]]:
        result = [
            result_as_dict(item)
            for item in get_result()
        ]
        return {'report': result}


class APIDrivers(Resource):
    def get(self) -> dict[str, list[dict[str, Any]]]:
        result = [
            {'id': item.id, 'abbr': item.abbr, 'name': item.name}
            for item in get_drivers()
        ]
        return {'drivers': result}


class APIDriver(Resource):
    def get(self, abbr: str) -> Response | dict[str, dict[str, Any]]:
        driver = get_driver(abbr)
        if driver is None:
            return Response(
                response={'Error': f'Driver with abbr {abbr} is not exists'},
                content_type='application/json',
                status=404
            )
        return {'driver_info': result_as_dict(driver)}
