import pytest


def test_result(client):
    result = client.get('/api/report/')
    
    for item in result.json['report']:
        assert 'place' in item
        assert 'name' in item
        assert 'start_time' in item
        assert 'end_time' in item
        assert 'result' in item

    assert len(result.json['report']) == 5
    assert result.status_code == 200


def test_drivers(client):
    drivers = client.get('/api/drivers/')
    for item in drivers.json['drivers']:
        assert 'id' in item
        assert 'name' in item
        assert 'abbr' in item
    
    assert len(drivers.json['drivers']) == 5
    assert drivers.status_code == 200


@pytest.mark.parametrize(
    'abbr, status',
    [('MES', 200), ('SPF', 200)]
)
def test_driver(client, abbr, status):
    driver = client.get(f'/api/driver/{abbr}')
    print(driver.json['driver_info']['place'])
    assert 'place' in driver.json['driver_info']
    assert 'abbr' in driver.json['driver_info']
    assert 'result' in driver.json['driver_info']
    assert driver.status_code == status


@pytest.mark.parametrize(
    'abbr, status',
    [('ABS', 404)]
)
def test_driver_is_none(client, abbr, status):
    driver = client.get(f'/api/driver/{abbr}')
    assert driver.status_code == status
