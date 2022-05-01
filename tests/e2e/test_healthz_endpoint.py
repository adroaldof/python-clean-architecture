"""End-to-end API tests"""
import pytest
import requests

from allocation.config import get_api_url


@pytest.mark.usefixtures("restart_api")
def test_returns_success_at_healthz_endpoint():
    url = get_api_url()
    response = requests.get(f"{url}/healthz")

    assert response.status_code == 200
