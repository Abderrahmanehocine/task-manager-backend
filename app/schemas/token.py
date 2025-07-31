from pydantic import BaseModel
from typing import Literal, Optional

class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"]

class TokenData(BaseModel):
    username: Optional[str] = None