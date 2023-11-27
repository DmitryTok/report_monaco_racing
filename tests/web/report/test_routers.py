import pytest


def test_index(client):
    index = client.get('/')
    
    assert b'Report Monaco Racing 2018' in index.data
    assert b'Report' in index.data
    assert b'Drivers' in index.data


def test_report(client):
    report = client.get('/report')
    
    assert b'Place' in report.data
    assert b'ABBR' in report.data
    assert b'Result' in report.data


def test_all_drivers(client):
    all_drivers = client.get('/drivers')
    
    assert b'Name' in all_drivers.data
    assert b'ABBR' in all_drivers.data
    assert b'Team' in all_drivers.data


@pytest.mark.parametrize(
    'abbr',
    ['MES']
)
def test_driver_info(client, abbr):
    driver = client.get(f'/driver/{abbr}')
    
    assert b'MES' in driver.data
    assert b'Marcus Ericsson' in driver.data
    assert b'60' in driver.data


@pytest.mark.parametrize('abbr', ['ABS'])
def test_driver_is_none(client, abbr):
    driver = client.get(f'/driver/{abbr}')
    
    assert b'Driver with abbr ABS, not exists' in driver.data
