"""End-to-end API tests"""
import pytest
import requests

from config import get_api_url
from test_mocks import mock_order_id, mock_reference, mock_sku


@pytest.mark.usefixtures("restart_api")
def test_returns_success_at_healthz_endpoint():
    url = get_api_url()
    response = requests.get(f"{url}/healthz")

    assert response.status_code == 200


@pytest.mark.usefixtures("restart_api")
def test_returns_created_201_and_allocated_batch_reference(add_stock):
    first_sku, second_sku = (mock_sku(), mock_sku())
    early_batch_ref, later_batch_ref, other_batch_ref = (
        mock_reference(),
        mock_reference(),
        mock_reference(),
    )

    add_stock(
        [
            (later_batch_ref, first_sku, 100, "2022-03-15"),
            (early_batch_ref, first_sku, 100, "2022-03-05"),
            (other_batch_ref, second_sku, 100, None),
        ]
    )

    url = f"{get_api_url()}/allocate"
    data = {"order_id": mock_order_id(), "sku": first_sku, "quantity": 3}

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.json()["reference"] == early_batch_ref
