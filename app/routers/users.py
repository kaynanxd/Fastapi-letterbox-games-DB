from fastapi import APIRouter, Depends, Query
from http import HTTPStatus

from app.schemas.user import (
    UserSchemaPublic,
    UserSchemaList,
    UserSchema,       
    UserSchemaUpdate,
)
from app.schemas.common import Message, FilterPage 

from app.dependencies import (
    UserServiceDep,
    CurrentUser,
    AdminUser
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    '/', 
    status_code=HTTPStatus.CREATED, 
    response_model=UserSchemaPublic, 
)

async def criar_usuario(user_schema: UserSchema, service: UserServiceDep):
    """Cria um novo usuário."""
    return await service.create_new_user(user_schema)

@router.get('/me', response_model=UserSchemaPublic)
async def ler_usuario_atual(current_user: CurrentUser):
    """Retorna os dados do usuário logado."""
    return current_user

@router.get('/todos', response_model=UserSchemaList)
async def ler_todos_usuarios(
    service: UserServiceDep,
    #admin: AdminUser,
    filter_params: FilterPage = Depends(FilterPage), 
    username: str | None = Query(None, description="Filtrar por nome de usuário"),
    email: str | None = Query(None, description="Filtrar por email"),
):
    """Lê a lista de usuários com paginação e filtros """
    
    return await service.get_all_users(
        offset=filter_params.offset, 
        limit=filter_params.limit,
        username=username,
        email=email
    )

@router.put('/atualizar/{user_id}', response_model=UserSchemaPublic)
async def atualizar_usuario(
    user_id: int,
    user_schema: UserSchemaUpdate,
    service: UserServiceDep,
    current_user: CurrentUser,
):
    """Atualiza um usuário."""
    return await service.update_existing_user(
        user_id=user_id, user_schema=user_schema, current_user=current_user
    )

@router.delete('/deletar/{user_id}', response_model=Message)
async def deletar_usuario(
    user_id: int,
    service: UserServiceDep,
    current_user: CurrentUser
):
    """Deleta um usuário."""
    message_dict = await service.delete_existing_user(
        user_id=user_id, 
        current_user=current_user
    )
    return message_dict

@router.post('/promover/{user_id}', response_model=UserSchemaPublic)
async def promover_usuario(
    user_id: int,
    service: UserServiceDep,
    #admin: AdminUser, 
):
    """Promove um usuário para admin"""
    user = await service.promote_user_to_admin(user_id=user_id)
    return user

@router.post('/rebaixar/{user_id}', response_model=UserSchemaPublic)
async def rebaixar_usuario(
    user_id: int,
    service: UserServiceDep,
    admin: AdminUser, 
):
    """Rebaixa um usuário de admin (Admin)."""
    user = await service.demote_user_from_admin(user_id=user_id)
    return user