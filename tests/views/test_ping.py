from httpx import Response
from http import HTTPStatus
from fastapi.testclient import TestClient


def test_ping(test_client: TestClient):
    resp: Response = test_client.get('/api/v1/ping')

    assert resp.status_code == HTTPStatus.OK
    assert resp.text == '{"message":"OK"}'


