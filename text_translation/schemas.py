from pydantic import BaseModel, EmailStr

class ClientCreate(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
