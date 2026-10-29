from typing import Optional ,Union,Literal
from pydantic import BaseModel, ValidationError , ConfigDict

class Order(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amount: int
    amount_due: int
    amount_paid:int
    attempts: int
    created_at: int
    currency: str
    entity: str
    id: str
    notes: Union[dict, list]
    offer_id: Optional[str]
    receipt: Optional[str]
    status:str

class ErrorDetail(BaseModel):
    
        code: str
        description: str
        metadata: dict
        reason: Optional[str]=None
        source: str
        step: Optional[str]=None

class ErrorResponse(BaseModel):
    error:ErrorDetail