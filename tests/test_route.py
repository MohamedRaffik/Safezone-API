from os import getenv

def test_routes_endpoint(client):
    res = client.get(f'/api/route/?origin_latitude=40.768515&origin_longitude=-73.964461&dest_latitude=40.740699&dest_longitude=-73.983167&API_KEY={getenv("API_KEY")}')
    assert '404' not in res.status
    assert '401' not in res.status
    assert '400' not in res.status
    data = res.get_json()
    for d in data:
        assert 'rating' in d
        assert type(d['rating']) == float
        assert 'leg' in d
        assert type(d['leg']) == dict
        assert 'lines' in d
        assert type(d['lines']) == list
        assert type(d['lines'][0]) == dict