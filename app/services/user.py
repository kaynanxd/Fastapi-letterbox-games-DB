from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

from app.repositories.user import UserRepository
from app.models.user import User
from app.schemas.user import UserSchemaUpdate,UserSchema
from app.security.security import get_password_hash


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository
    

    async def create_new_user(self, user_schema: UserSchema) -> User:

        db_user = await self.repository.get_by_email_or_username(
            email=user_schema.email, username=user_schema.username
        )
        
        if db_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username or Email already registered"
            )
        
        hashed_password = get_password_hash(user_schema.password)

        new_user = User(
            email=user_schema.email,
            username=user_schema.username,
            password=hashed_password,
        )
        
        db_user = await self.repository.create_user(new_user)

        return db_user

    async def get_all_users(
            self, 
            offset: int, 
            limit: int,
            username: str | None = None,
            email: str | None = None,
        ) -> dict:
            """
            Busca todos os usuários com paginação e filtros.
            Retorna um dicionário pronto para o schema UserSchemaList.
            """
            users_list, total_count = await self.repository.get_users_paginated(
                offset=offset, limit=limit, username=username, email=email
            )
            
            return {
                'items': users_list,
                'total': total_count
            }
        
    
    async def update_existing_user(
            self, user_id: int, user_schema: UserSchemaUpdate, current_user: User
        ) -> User:
            
            is_owner = (current_user.id == user_id)
            is_admin = current_user.admin

            if not is_admin and not is_owner:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
                )

            user_to_update = await self.repository.get_by_id(user_id)
            if not user_to_update:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="User not found"
                )

            update_data = user_schema.model_dump(exclude_unset=True)
            
            try:
                if 'password' in update_data:
                    user_to_update.password = get_password_hash(update_data['password'])

                if 'email' in update_data:
                    user_to_update.email = update_data['email']

                if 'username' in update_data:
                    user_to_update.username = update_data['username']

                return await self.repository.update_user(user_to_update)
            
            except IntegrityError:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail='Username or Email already exists',
                )
            

    async def delete_existing_user(
            self, user_id: int, current_user: User
        ):
            
            user_to_delete = await self.repository.get_by_id(user_id)
            if not user_to_delete:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="User not found"
                )

            is_owner = (current_user.id == user_to_delete.id)
            is_admin = current_user.admin

            if not is_admin and not is_owner:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
                )
                
            await self.repository.hard_delete_user(user_to_delete)
            return {"message": "User permanently deleted"}
            
            
    async def promote_user_to_admin(self, user_id: int) -> User:
        
        user_to_promote = await self.repository.get_by_id(user_id)
        if not user_to_promote:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )

        if user_to_promote.admin:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, 
                detail="User is already an admin"
            )

        user_to_promote.admin = True
        return await self.repository.update_user(user_to_promote)

    async def demote_user_from_admin(self, user_id: int) -> User:
        
        user_to_demote = await self.repository.get_by_id(user_id)
        if not user_to_demote:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )

        if not user_to_demote.admin:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, 
                detail="User is not an admin"
            )

        user_to_demote.admin = False
        return await self.repository.update_user(user_to_demote)
    