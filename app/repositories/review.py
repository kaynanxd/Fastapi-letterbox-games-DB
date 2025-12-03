from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.user import Avaliacao, Jogo 

class ReviewRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_review(self, review: Avaliacao) -> Avaliacao:
        stmt = text("""
            INSERT INTO avaliacoes (nota, comentario, id_jogo, id_user)
            VALUES (:nota, :comment, :jid, :uid)
            RETURNING id_avaliacao
        """)
        
        params = {
            "nota": review.nota,
            "comment": review.comentario,
            "jid": review.id_jogo,
            "uid": review.id_user
        }
        
        result = await self.session.execute(stmt, params)
        review.id_avaliacao = result.scalar()
        await self.session.commit()
        return review

    async def get_reviews_by_game(self, game_id: int) -> list[dict]:
        stmt = text("""
            SELECT a.id_avaliacao, a.nota, a.comentario, a.id_jogo, a.id_user, u.username
            FROM avaliacoes a
            JOIN users u ON a.id_user = u.id
            WHERE a.id_jogo = :jid
        """)
        
        result = await self.session.execute(stmt, {"jid": game_id})
        
        reviews = []
        for row in result.mappings():
            reviews.append(dict(row))
        return reviews
    
    async def get_reviews_by_user(self, user_id: int) -> list[Avaliacao]:
            stmt = (
                select(Avaliacao)
                .where(Avaliacao.id_user == user_id)
                .options(
                    joinedload(Avaliacao.jogo) 
                )
            )
            result = await self.session.execute(stmt)
            return result.scalars().all()
    
    async def get_by_user_and_game(self, user_id: int, game_id: int) -> Avaliacao | None:
        stmt = select(Avaliacao).where(
            Avaliacao.id_user == user_id, 
            Avaliacao.id_jogo == game_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_review(self, review: Avaliacao) -> Avaliacao:
        await self.session.commit()
        await self.session.refresh(review)
        return review
    
    async def get_by_id(self, review_id: int) -> Avaliacao | None:
        stmt = select(Avaliacao).where(Avaliacao.id_avaliacao == review_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def delete_review_by_id(self, review_id: int):
        stmt = text("DELETE FROM avaliacoes WHERE id_avaliacao = :id")
        await self.session.execute(stmt, {"id": review_id})
        await self.session.commit()