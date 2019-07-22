from os import getenv

def test_crimes_endpoint(client):
    res = client.get(f'/api/crimes/nearby?latitude=12&longitude=12&API_KEY={getenv("API_KEY")}')
    assert '404' not in res.status
    assert '401' not in res.status
    assert '400' not in res.status
    data = res.get_json()
    assert 'frequencies' and 'results' in data
    assert type(data['frequencies']) == dict
    assert type(data['results']) == list