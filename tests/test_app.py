from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_read_root():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, Mundo!'}


def test_exercicio_aula_02():
    client = TestClient(app)
    response = client.get('/exercicio-html')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo, em formato HTML!</h1>' in response.text
