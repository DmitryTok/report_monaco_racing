import operator
import simplexml
from flask import request, jsonify
from flask_restful import Resource
from .models import Drivers, Time


RACING_DATA = 'data/'


class Index(Resource):

    def get(self):
        if request.args.get('format') == 'xml':
            return simplexml.dumps({'data': {'title': 'Report Monaco Racing 2018'}})
        return jsonify('Report Monaco Racing 2018')


class ReportRacing(Resource):

    def get(self):
        """
        Racing report
        ---
        responses:
          200:
            description: Sorted racing report
        """
        query = Time.select().join(Drivers)
        drivers_dict = {}
        for i in query:
            drivers_dict[i.code.code + ' | ' + i.code.name] = str(i.end - i.start)
            # d_list = str(i.code.code + ' | ' + i.code.name + ' : ' + i.end - i.start)
        asc = sorted(drivers_dict.items(), key=operator.itemgetter(1))
        desc = sorted(drivers_dict.items(), key=operator.itemgetter(1), reverse=True)
        if request.args.get('format') == 'xml':
            return simplexml.dumps({'data':drivers_dict})
        if request.args.get('order') == 'desc':
            return jsonify(desc)
        else:
            return jsonify(asc)


class ReportDrivers(Resource):

    def get(self):
        """
        Report drivers
        ---
        responses:
          200:
            description: List with a drivers
        """
        query = Drivers.select()
        code_name_dict = {}
        for item in query:
            code_name_dict[item.code] = item.name
        asc = sorted(code_name_dict.items(), key=operator.itemgetter(0))
        desc = sorted(code_name_dict.items(), key=operator.itemgetter(0), reverse=True)
        if request.args.get('format') == 'xml':
            return simplexml.dumps({'data': code_name_dict})
        if request.args.get('order') == 'desc':
            return jsonify(desc)
        else:
            return jsonify(asc)


class ReportDriversCode(Resource):

    def get(self, driver_code):
        """
        Report drivers code
        ---
        parameters:
          - name: driver_code
            in: path
            type: string
            required: true
        responses:
          200:
            description: Info about driver
        """
        query = Time.select().join(Drivers)
        drivers_dict = {}
        for item in query:
            drivers_dict[str(item.code.code + ' | ' + item.code.name)] = str(item.end - item.start)
        for name, time in drivers_dict.items():
            if driver_code in name:
                return f'{name} | {time}'
        if request.args.get('format') == 'xml':
            return simplexml.dumps(drivers_dict)
        else:
            return jsonify(drivers_dict)
