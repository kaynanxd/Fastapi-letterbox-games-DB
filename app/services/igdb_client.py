import httpx
from datetime import datetime, timedelta
from fastapi import HTTPException
from http import HTTPStatus

class IGDBClient:
    BASE_URL = "https://api.igdb.com/v4"
    AUTH_URL = "https://id.twitch.tv/oauth2/token"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None

    async def _authenticate(self):
        """Obtém um novo token de acesso se o atual expirou ou não existe."""
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.AUTH_URL,
                params={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials",
                },
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                    detail="Falha ao autenticar com IGDB. Verifique as credenciais.",
                )

            data = response.json()
            self.access_token = data["access_token"]
            self.token_expires_at = datetime.now() + timedelta(seconds=data["expires_in"] - 60)

    async def search_games(self, query: str, limit: int = 20, offset: int = 0) -> list[dict]:
            """Busca jogos no IGDB pelo nome com paginação."""
            await self._authenticate()

            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.access_token}",
            }

            fields = "name, cover.url, summary, screenshots.url, artworks.url, videos.video_id"
            
            body = f'search "{query}"; fields {fields}; limit {limit}; offset {offset};'

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/games",
                    headers=headers,
                    data=body
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=HTTPStatus.BAD_GATEWAY,
                        detail="Erro ao buscar jogos no IGDB",
                    )
                
                return response.json()

    async def get_game_by_id(self, game_id: int) -> dict | None:
        """
        Busca detalhes completos de um jogo, incluindo Empresas e DLCs.
        """
        await self._authenticate()
        
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }
        
        fields = (
                    "name, cover.url, summary, aggregated_rating, genres.name, "
                    "platforms.name, first_release_date, "
                    "involved_companies.company.name, "
                    "involved_companies.company.country, "
                    "involved_companies.company.start_date, "
                    "involved_companies.developer, involved_companies.publisher, "
                    "dlcs.name, dlcs.summary,"
                    "screenshots.url, artworks.url, videos.video_id"
                )
        
        body = f'fields {fields}; where id = {game_id};'
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/games",
                headers=headers,
                data=body
            )
            
            if response.status_code != 200:
                 raise HTTPException(
                    status_code=HTTPStatus.BAD_GATEWAY,
                    detail="Erro ao buscar detalhes do jogo no IGDB",
                )
            
            data = response.json()
            return data[0] if data else None
    