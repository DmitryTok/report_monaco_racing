from http import HTTPStatus
from racing_report.web_report import app


client = app.test_client()


def test_urls():
    urls = {
        '/': HTTPStatus.OK,
        '/report/': HTTPStatus.OK,
        '/report/?order=desc': HTTPStatus.OK,
        '/report/drivers/': HTTPStatus.OK,
        '/report/drivers/?order=desc': HTTPStatus.OK,
        '/report/drivers/DRR/': HTTPStatus.OK,
        '/unexpected_page/': HTTPStatus.NOT_FOUND
    }
    for adress, code in urls.items():
        response = client.get(adress)
        assert response.status_code == code


def test_index_data():
    call = client.get('/')
    assert b'<a class="nav-link" href="/report/">' in call.data
    assert b'<a class="nav-link" href="/report/drivers/">' in call.data


def test_report_data():
    call = client.get('report/')
    assert b'DRR | Daniel Ricciardo | RED BULL RACING TAG HEUER : -1 day, 23:57:12.013000' in call.data
    assert b'SSW | Sergey Sirotkin | WILLIAMS MERCEDES : -1 day, 23:55:12.706000' in call.data
    assert b'RGH | Romain Grosjean | HAAS FERRARI : 0:01:12.930000' in call.data


def test_report_desc():
    call = client.get('/report/?order=desc')
    assert b'CSR | Carlos Sainz | RENAULT : 0:01:12.950000' in call.data
    assert b'SVM | Stoffel Vandoorne | MCLAREN RENAULT : 0:01:12.463000' in call.data
    assert b'CLS | Charles Leclerc | SAUBER FERRARI : 0:01:12.829000' in call.data


def test_report_drivers_data():
    call = client.get('/report/drivers/')
    assert b'| Lewis Hamilton | MERCEDES' in call.data
    assert b'| Brendon Hartley | SCUDERIA TORO ROSSO HONDA' in call.data


def test_report_drivers_desc():
    call = client.get('/report/drivers/?order=desc')
    assert b'| Esteban Ocon | FORCE INDIA MERCEDES' in call.data
    assert b'| Kevin Magnussen | HAAS FERRARI' in call.data


def test_driver_info():
    call_CSR = client.get('/report/drivers/CSR/')
    assert b'CSR | Carlos Sainz | RENAULT : 0:01:12.950000' in call_CSR.data


def test_unexpected_page():
    call = client.get('/unexpected_page/')
    assert b'p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>' in call.data
