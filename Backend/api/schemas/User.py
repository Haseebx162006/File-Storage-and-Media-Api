from pydantic import EmailStr, Field, BaseModel


class Create_User_Schema(BaseModel):
    email:EmailStr
    password:str=Field(min_length=6)
    name:str
    
class Read_User_Schema(BaseModel):
    id: int
    email:str
    name:str
    
    class Config:
        form_attributes=True
    
class Update_User_Schama():
    email:EmailStr
    password:str=Field(min_length=6)
    name: str
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"