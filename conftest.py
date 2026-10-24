import os
import pytest
import requests
from configs.constants import BASE_URL , KEY_ID, KEY_SECRET
from api.client import ApiClient

@pytest.fixture
def api_client():
    return ApiClient()

@pytest.fixture
def create_order(api_client):
    payload={
            
                "amount": 500,
                "currency": "INR"
            
        }
    response=api_client.post("/v1/orders",payload)
    return response.json() 

