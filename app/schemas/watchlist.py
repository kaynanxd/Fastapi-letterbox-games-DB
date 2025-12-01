from pydantic import BaseModel
from datetime import date

class GenrePublic(BaseModel):
    id_genero: int
    nome_genero: str
    class Config: from_attributes = True

class PlatformPublic(BaseModel):
    id_plataforma: int
    nome: str
    class Config: from_attributes = True

class JogoPlataformaPublic(BaseModel):
    data_lancamento: date | None = None
    plataforma: PlatformPublic
    
    class Config: from_attributes = True

class CompanyPublic(BaseModel):
    id_empresa: int
    nome: str
    pais_origem: str | None = None
    mercado_principal: str | None = None
    class Config: from_attributes = True
    

class DLCPublic(BaseModel):
    nome_dlc: str
    descricao: str | None = None
    class Config: from_attributes = True

class GameDetailsPublic(BaseModel):
    id_jogo: int
    titulo: str
    descricao: str | None = None
    nota_metacritic: int | None = None
    
    desenvolvedora: CompanyPublic | None = None
    publicadora: CompanyPublic | None = None
    generos: list[GenrePublic] = []
    dlcs: list[DLCPublic] = []


    plataformas_associacao: list[JogoPlataformaPublic] = [] 

    class Config:
        from_attributes = True


class IGDBGameResult(BaseModel):
    id: int
    name: str
    summary: str | None = None
    cover_url: str | None = None
    screenshots: list[str] = [] 
    videos: list[str] = []     

class IGDBGameList(BaseModel):
    results: list[IGDBGameResult]

class WatchlistCreate(BaseModel):
    """Agora exige um nome para criar a watchlist."""
    nome: str 

class WatchlistPublic(BaseModel):
    """Retorno público atualizado."""
    id_watchlist: int
    id_user: int
    nome: str | None = None
    
    jogos: list[GameDetailsPublic] = [] 

    class Config:
        from_attributes = True

        


class WatchlistPublic2(BaseModel):
    """Retorno público atualizado."""
    id_watchlist: int
    id_user: int
    nome: str | None = None 


    class Config:
        from_attributes = True

class AddGameToWatchlist(BaseModel):
    igdb_game_id: int
