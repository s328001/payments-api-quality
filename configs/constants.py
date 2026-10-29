import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL=os.getenv("BASE_URL","https://api.razorpay.com")
KEY_ID=os.getenv("key_id")
KEY_SECRET = os.getenv("key_secret")

VALID_PAYLOAD={
    "amount":500,
    "currency":"INR"
}