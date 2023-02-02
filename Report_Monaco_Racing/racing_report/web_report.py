import operator
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_restful import Api
from .api_web_report import ReportRacing, ReportDrivers, ReportDriversCode, Index
from flasgger import Swagger
from .models import Drivers, Time

app = Flask(__name__)
api = Api(app)
Bootstrap(app)
Swagger(app)
RACING_DATA = 'data/'


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/report/')
def report():
    query = Time.select().join(Drivers)
    drivers_dict = {}
    for i in query:
        drivers_dict[i.code.code, i.code.name] = str(i.end - i.start)
    asc = sorted(drivers_dict.items(), key=operator.itemgetter(1))
    desc = sorted(drivers_dict.items(), key=operator.itemgetter(1), reverse=True)
    if request.args.get('order') == 'desc':
        racers_list = desc
    else:
        racers_list = asc
    return render_template('report.html', racers_list=racers_list)


@app.route('/report/drivers/')
def report_driver():
    query = Drivers.select()
    code_name_list = []
    for item in query:
        a = str(item.code + ' | ' + item.name)
        code_name_list.append(a)
    asc = sorted(code_name_list)
    desc = sorted(code_name_list, reverse=True)
    if request.args.get('order') == 'desc':
        driver_list = desc
    else:
        driver_list = asc
    return render_template('drivers.html', driver_list=driver_list)


@app.route('/report/drivers/<string:driver_code>/')
def driver_info(driver_code):
    query = Time.select().join(Drivers)
    drivers_lict = []
    for item in query:
        conct = str(item.code.code + ' | ' + item.code.name + ' : ' + str(item.end - item.start))
        drivers_lict.append(conct)
    for elem in drivers_lict:
        if driver_code in elem:
            return elem
    return render_template('about_driver.html', elem=elem)


api.add_resource(Index, '/api/v1/')
api.add_resource(ReportRacing, '/api/v1/report/')
api.add_resource(ReportDrivers, '/api/v1/report/drivers/')
api.add_resource(ReportDriversCode, '/api/v1/report/drivers/<driver_code>')
