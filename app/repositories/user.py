from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email_or_username(
        self, email: str, username: str
    ) -> User | None:
        """
        Busca um usuário por email OU username.
        """
        stmt = text("""
            SELECT id, username, email, password, admin 
            FROM users 
            WHERE email = :email OR username = :username
            LIMIT 1
        """)
        
        result = await self.session.execute(stmt, {"email": email, "username": username})
        row = result.mappings().first()
        
        if row:
            user = User(
                username=row.username,
                email=row.email,
                password=row.password
            )
            user.id = row.id 
            user.admin = bool(row.admin)
            return user
            
        return None

    async def get_users_paginated(
            self, 
            offset: int, 
            limit: int,
            username: str | None = None,
            email: str | None = None,
        ) -> tuple[list[User], int]:
            """
            Busca usuários com paginação e filtros.
            """
            base_query = "SELECT id, username, email, password, admin FROM users WHERE 1=1"
            count_query = "SELECT count(*) FROM users WHERE 1=1"
            params = {"limit": limit, "offset": offset}

            if username:
                base_query += " AND username LIKE :username"
                count_query += " AND username LIKE :username"
                params["username"] = f"%{username}%"
            
            if email:
                base_query += " AND email LIKE :email"
                count_query += " AND email LIKE :email"
                params["email"] = f"%{email}%"
                
            base_query += " LIMIT :limit OFFSET :offset"
            
            result_rows = await self.session.execute(text(base_query), params)
            result_total = await self.session.execute(text(count_query), params)
            
            total = result_total.scalar()
            
            users = []
            for row in result_rows.mappings():
                u = User(
                    username=row.username,
                    email=row.email,
                    password=row.password
                )
                u.id = row.id
                u.admin = bool(row.admin)
                users.append(u)
            
            return users, total or 0

    async def create_user(self, user: User) -> User:
        """Cria um novo usuário"""
        stmt = text("""
            INSERT INTO users (username, email, password, admin)
            VALUES (:username, :email, :password, :admin)
            RETURNING id
        """)
        
        params = {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "admin": user.admin
        }
        
        result = await self.session.execute(stmt, params)
        new_id = result.scalar()
        await self.session.commit()
        
        user.id = new_id
        return user

    async def update_user(self, user: User) -> User:
        """Atualiza um usuário existente usando UPDATE SQL."""
        stmt = text("""
            UPDATE users 
            SET username = :username, email = :email, password = :password, admin = :admin
            WHERE id = :id
        """)
        
        params = {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "admin": user.admin,
            "id": user.id
        }
        
        await self.session.execute(stmt, params)
        await self.session.commit()
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        """Busca um usuário pelo ID"""
        stmt = text("SELECT id, username, email, password, admin FROM users WHERE id = :id")
        result = await self.session.execute(stmt, {"id": user_id})
        row = result.mappings().first()
        
        if row:
            u = User(
                username=row.username,
                email=row.email,
                password=row.password
            )
            u.id = row.id
            u.admin = bool(row.admin)
            return u
        return None
    
    async def get_by_email(self, email: str) -> User | None:
        """Busca um usuário pelo Email."""
        stmt = text("SELECT id, username, email, password, admin FROM users WHERE email = :email")
        result = await self.session.execute(stmt, {"email": email})
        row = result.mappings().first()
        
        if row:
            u = User(
                username=row.username,
                email=row.email,
                password=row.password
            )
            u.id = row.id
            u.admin = bool(row.admin)
            return u
        return None

    async def hard_delete_user(self, user: User) -> None:
        """Deleta um usuário permanentemente"""
        stmt = text("DELETE FROM users WHERE id = :id")
        await self.session.execute(stmt, {"id": user.id})
        await self.session.commit()