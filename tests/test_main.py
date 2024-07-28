def test_get_main(test_client):
    response = test_client.post('/')
    assert response.status_code == 200
    assert response.json() == {'Ganesha': 'Key ?'}
