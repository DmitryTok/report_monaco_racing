from http import HTTPStatus
from racing_report.web_report import app


client = app.test_client()


def test_status_codes():
    urls = {
        '/api/v1/': HTTPStatus.OK,
        '/api/v1/?format=xml': HTTPStatus.OK,
        '/api/v1/report/': HTTPStatus.OK,
        '/api/v1/report/?format=xml': HTTPStatus.OK,
        '/api/v1/report/?order=desc': HTTPStatus.OK,
        '/api/v1/report/drivers/': HTTPStatus.OK,
        '/api/v1/report/drivers/?format=xml': HTTPStatus.OK,
        '/api/v1/report/drivers/?order=desc': HTTPStatus.OK,
        '/api/v1/report/drivers/SVF': HTTPStatus.OK,
        '/api/v1/report/drivers/SVF?format=xml': HTTPStatus.OK,
        '/api/v1/unexpected_page': HTTPStatus.NOT_FOUND
    }
    for adress, code in urls.items():
        response = client.get(adress)
        assert response.status_code == code


def test_index():
    call = client.get('/api/v1/')
    call_xml = client.get('/api/v1/?format=xml')
    assert call.get_data() == b'"Report Monaco Racing 2018"\n'
    assert call_xml.get_data() == b'"<?xml version=\\"1.0\\" ?><data><title>Report Monaco Racing 2018</title></data>"\n'


def test_report_resource():
    call = client.get('/api/v1/report/')
    call_xml = client.get('/api/v1/report/?format=xml')
    call_desc = client.get('/api/v1/report/?order=desc')
    assert b'LHM | Lewis Hamilton | MERCEDES","-1 day, 23:53:12.460000' in call.data
    assert b'SVF | Sebastian Vettel | FERRARI>0:01:04.415000' in call_xml.data
    assert b'KMH | Kevin Magnussen | HAAS FERRARI","0:01:13.393000' in call_desc.data
        

def test_report_drivers_resource():
    call = client.get('/api/v1/report/drivers/')
    call_xml = client.get('/api/v1/report/drivers/?format=xml')
    call_desc = client.get('/api/v1/report/drivers/?order=desc')
    assert b'"BHS","Brendon Hartley | SCUDERIA TORO ROSSO HONDA' in call.data
    assert b'<SVF>Sebastian Vettel | FERRARI</SVF>' in call_xml.data
    assert b'"VBM","Valtteri Bottas | MERCEDES"' in call_desc.data


def test_drivers_code_resource():
    call = client.get('/api/v1/report/drivers/BSH')
    assert b'"BHS | Brendon Hartley | SCUDERIA TORO ROSSO HONDA":"0:01:13.179000"' in call.data    


def test_unexpected_resource():
    call = client.get('/api/v1/unexpected_page')
    assert b'404 Not Found' in call.data
