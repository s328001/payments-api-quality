import os 
import requests
from dotenv import load_dotenv
from configs.constants import BASE_URL ,KEY_ID ,KEY_SECRET
load_dotenv()

def test_create_order_with_valid_data():
        url=f"{BASE_URL}/v1/orders"
        payload={
            
                "amount": 500,
                "currency": "INR"
            
        }
        response=requests.post(url,
                            auth=(KEY_ID,KEY_SECRET),
                            json=payload,timeout=10)
        assert response.status_code==200,response.text
        
        body=response.json()
        assert body["status"]=="created"
        assert body["amount"]==payload["amount"]
        assert body["currency"]==payload["currency"]
        assert body["id"].startswith("order_")