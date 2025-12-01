from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    nota: float = Field(..., ge=0, le=10)
    comentario: str | None = Field(None, max_length=1000)

class ReviewPublic(BaseModel):
    id_avaliacao: int
    nota: float
    comentario: str | None
    id_jogo: int
    id_user: int
    
    class Config: from_attributes = True

class ReviewGameInfo(BaseModel):
    id_jogo: int
    titulo: str
    class Config: from_attributes = True

class MyReviewPublic(BaseModel):
    id_avaliacao: int
    nota: float
    comentario: str | None = None
    
    jogo: ReviewGameInfo | None = None 

    class Config:
        from_attributes = True

class ReviewList(BaseModel):
    items: list[ReviewPublic]
    media_nota: float | None = None