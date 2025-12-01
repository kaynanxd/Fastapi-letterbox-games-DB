"""
Schemas para Tokens (Input/Output)
"""
from pydantic import BaseModel

class Token(BaseModel):
    """
    Schema de resposta para o endpoint de login (/auth/token).
    Contém ambos os tokens.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AccessToken(BaseModel):
    """
    Schema de resposta para o endpoint de refresh (/auth/refresh_token).
    Contém apenas o novo access token.
    """
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """
    Schema interno para os dados (payload) dentro do JWT.
    """
    sub: str | None = None 