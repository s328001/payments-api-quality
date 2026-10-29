import requests
import pytest
from configs.constants import BASE_URL ,KEY_ID ,KEY_SECRET , VALID_PAYLOAD

def test_empty_auth(api_client):
        
        response=api_client.post_without_auth("/v1/orders",VALID_PAYLOAD)
        assert response.status_code==401,response.text
        body=response.json()
        
        assert body["error"]["description"]=="Please provide your api key for authentication purposes"
        
@pytest.mark.parametrize( "key_id, key_secret",
                        [("rzp_test_fakeid123","fakesecret123"),
                        (KEY_ID,"fakeseret123"),
                        ("","")
                        ])
def test_wrong_auth(key_id, key_secret):

        
        response = requests.post(url=f"{BASE_URL}/v1/orders",json=VALID_PAYLOAD, auth=(key_id, key_secret))
        assert response.status_code==401,response.text
        body=response.json()
        assert body["error"]["description"]=="Authentication failed"
        assert body["error"]["code"]=="BAD_REQUEST_ERROR"
