from os import getenv

def test_nearby_stations_endpoint(client):
    res = client.get(f'/api/stations/nearby?latitude=40.768515&longitude=-73.964461&API_KEY={getenv("API_KEY")}')
    assert '404' not in res.status
    assert '401' not in res.status
    assert '400' not in res.status
    data = res.get_json()
    for d in data:
        assert 'id' in d
        assert type(d['id']) == int
        assert 'latitude' in d
        assert type(d['latitude']) == float
        assert 'longitude' in d
        assert type(d['longitude']) == float
        assert 'lines' in d
        assert type(d['lines']) == list
        assert 'name' in d
        assert type(d['name']) == str
        assert 'percentile' in d
        assert type(d['percentile']) == float

def test_nearby_crimes_station_endpoint(client):
    res = client.get(f'/api/stations/nearby_crimes?id=1&API_KEY={getenv("API_KEY")}')
    assert '404' not in res.status
    assert '401' not in res.status
    assert '400' not in res.status
    data = res.get_json()
    assert 'frequencies' and 'results' in data
    assert type(data['frequencies']) == dict
    assert type(data['results']) == list