import requests
import pytest
from configs.constants import VALID_PAYLOAD
from api.schema import Order , ErrorResponse

def test_create_order_with_valid_data(api_client):
        
        response=api_client.post("/v1/orders",VALID_PAYLOAD)
        
        assert response.status_code==200,response.text
        
        order=Order.model_validate(response.json())
        
        assert order.status=="created"
        assert order.amount==VALID_PAYLOAD["amount"]
        assert order.currency==VALID_PAYLOAD["currency"]
        assert order.id.startswith("order_")
        assert order.amount_due==order.amount
        assert order.amount_paid == 0
        assert order.attempts == 0

        
        
@pytest.mark.parametrize("expected_amount,expected_currency",
                [
                        (599,"INR"),
                        (1000,"USD")
                ]
        )
def test_create_order_with_valid_amounts(api_client,expected_amount,expected_currency):        
        payload={
                "amount":expected_amount,
                "currency":expected_currency
        }
        response=api_client.post("/v1/orders",payload)
        assert response.status_code==200,response.text
        
        order=Order.model_validate(response.json())
        
        assert order.status=="created"
        assert order.amount==expected_amount
        assert order.currency==expected_currency
        assert order.id.startswith("order_")
        assert order.amount_due==order.amount
        assert order.amount_paid == 0
        assert order.attempts == 0
        

@pytest.mark.parametrize("amount,currency,description",
                [
                        (599.99,"INR","The amount must be an integer."),
                        (-1,"INR","amount: must be no less than 0."),
                        (-599.99,"INR","The amount must be an integer."),
                        (500,"RGB","currency: validation_failure: BAD_REQUEST_INVALID_CURRENCY."),
                        (0,"INR","Order amount less than minimum amount allowed"),
                        (1,"INR","Order amount less than minimum amount allowed"),
                ]
                #, ids=["decimal", "negative", "negative_decimal", "invalid_currency", "zero", "one_paisa", "below_min"],

        )
def test_create_order_with_invalid_input(api_client,amount,currency,description):
        payload={
                "amount":amount,
                "currency":currency
        }
        response=api_client.post("/v1/orders",payload)
        
        assert response.status_code==400,response.text
        
        error=ErrorResponse.model_validate(response.json()).error
        assert error.code=="BAD_REQUEST_ERROR"
        assert error.description==description

        
def test_create_order_with_unknown_field(api_client):
        payload={
                "amount":500,
                "currency":"INR",
                "unknown_field":"unknown_field"
                
        }
        response=api_client.post("/v1/orders",payload)
        
        assert response.status_code==400,response.text
        error=ErrorResponse.model_validate(response.json()).error
        assert error.code=="BAD_REQUEST_ERROR"
        assert error.description=="unknown_field is/are not required and should not be sent"
        assert error.reason=="extra_field_sent"
        




