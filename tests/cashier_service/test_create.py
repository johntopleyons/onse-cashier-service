import pytest
from unittest.mock import Mock
import json

from cashier_service.app import create
from cashier_service.mock.mock_events import MockEvents
from cashier_service.settings import config


@pytest.fixture(scope='function')
def web_client(logger):
    broker = MockEvents()
    return create(config=config['testing'], broker=broker, logger=logger).test_client()


@pytest.fixture(scope='function')
def logger():
    return Mock()


def test_should_process_client_request(web_client):
    payload = {
        "accountNumber": "some-acc-number",
        "amount": 10815,
        "action": "withdrawn"
    }
    response = web_client.post(
        '/cashier/create', json=json.loads(json.dumps(payload)))
    assert response.status_code == 201, \
        f'Expected status code to be 201; got {response.status_code}'
    assert response.is_json, \
        f'Expected content type to be JSON; got "{response.data}'
    assert response.get_json()[
        'accountNumber'] == 'some-acc-number', f'Unexpected JSON; got {repr(response.get_json())} '
