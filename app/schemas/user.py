
from pydantic import BaseModel, EmailStr, Field, model_validator


class UserSchemaPublic(BaseModel):
    """
    Schema para retornar dados PÚBLICOS do usuário.
    (Sem senha, sem dados sensíveis)
    
    CAMPOS REMOVIDOS (is_active, created_at) para bater com o Model.
    """
    id: int
    username: str
    email: EmailStr
    admin: bool
    

    class Config:
        from_attributes = True


class UserSchemaList(BaseModel):
    """
    Schema de resposta para listas paginadas de usuários.
    """
    items: list[UserSchemaPublic]
    total: int


class UserSchema(BaseModel):
    """
    Schema para CRIAR um novo usuário.
    Usado pelo seu 'create_new_user'
    """
    username: str
    email: EmailStr
    password: str


class UserSchemaUpdate(BaseModel):
    """
    Schema para ATUALIZAR um usuário (parcial).
    Usado pelo seu 'update_existing_user'
    Todos os campos são opcionais.
    """
    username: str | None = None
    email: EmailStr | None = None

    password: str | None = Field(default=None)

class UserChangePasswordSchema(BaseModel):
    """
    Schema para o PRÓPRIO usuário alterar sua senha.
    Usado pelo seu 'change_user_password'
    """
    old_password: str
    new_password: str = Field(min_length=8)
    new_password_confirmation: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        pw1 = self.new_password
        pw2 = self.new_password_confirmation
        if pw1 is not None and pw1 != pw2:
            raise ValueError('A nova senha e a confirmação não batem.')
        return self

class UserEmailChangeRequestSchema(BaseModel):
    """
    Schema para solicitar mudança de email.
    (Importado pelo seu service, mas ainda não implementado)
    """
    new_email: EmailStr