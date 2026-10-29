from configs.constants import BASE_URL , KEY_ID, KEY_SECRET 
import requests
class ApiClient:
    def __init__(self):
        self.url=BASE_URL
        self.id=KEY_ID
        self.secret=KEY_SECRET
        self.session = requests.Session()
        
    def post(self,path,payload):
        return self.session.post(url=f"{self.url}{path}",auth=(self.id,self.secret),
                            json=payload,timeout=10)
    def get(self,path):
        return self.session.get(url=f"{self.url}{path}",auth=(self.id,self.secret))
    
    def post_without_auth(self,path,payload):
        return self.session.post(url=f"{self.url}{path}",json=payload)