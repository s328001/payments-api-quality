import requests
import pytest
from configs.constants import BASE_URL ,KEY_ID ,KEY_SECRET , VALID_PAYLOAD

def test_fetch_order_by_id(create_order,api_client):
        order_id=create_order["id"]
        response=api_client.get(f"/v1/orders/{order_id}")
        
        assert response.status_code==200,response.text
        
        body=response.json()
        assert body["id"]==order_id
        assert body["amount"] == create_order["amount"]

def test_fetch_non_existant_order(api_client):
        suffix= "doesnotexist123"
        order_id=f"order_{suffix}"
        response=api_client.get(f"/v1/orders/{order_id}")
        
        assert response.status_code==400,response.text
        body=response.json()
        assert body["error"]["description"]==f"{suffix} is not a valid id"
        assert body["error"]["code"]=="BAD_REQUEST_ERROR"
        assert body["error"]["reason"]=="input_validation_failed"
