from pydantic import BaseModel

class LoginRequest(BaseModel):
    cnpj: str
    password: str
