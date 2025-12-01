"""
Schemas para Autenticação (Input)
"""
from pydantic import BaseModel, Field, model_validator

class ResetPasswordSchema(BaseModel):
    """
    Schema para o corpo da requisição de reset de senha.
    Usado pelo seu AuthService.
    """
    new_password: str = Field(min_length=8)
    new_password_confirmation: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        """Validador para garantir que as senhas batem."""
        pw1 = self.new_password
        pw2 = self.new_password_confirmation
        
        if pw1 is not None and pw1 != pw2:
            raise ValueError('A nova senha e a confirmação não batem.')
        return self