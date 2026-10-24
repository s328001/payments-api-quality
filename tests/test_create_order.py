import requests
from configs.constants import BASE_URL ,KEY_ID ,KEY_SECRET
# from api.client import ApiClient

def test_create_order_with_valid_data(api_client):
        # url=f"{BASE_URL}/v1/orders"
        payload={ 
                "amount": 500,
                "currency": "INR"
        }

        response=api_client.post("/v1/orders",payload)
        
        body=response.json()
        assert response.status_code==200,response.text
        assert body["status"]=="created"
        assert body["amount"]==payload["amount"]
        assert body["currency"]==payload["currency"]
        assert body["id"].startswith("order_")
        
def test_fetch_order_by_id(create_order,api_client):
        order_id=create_order["id"]
        
        response=api_client.get("/v1/orders/"f"{order_id}")
        assert response.status_code==200,response.text
        body=response.json()
        assert body["id"]==order_id
        assert body["amount"] == create_order["amount"]