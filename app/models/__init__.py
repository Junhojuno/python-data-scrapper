from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import (
    NAVER_MONGO_DB_NAME, NAVER_MONGO_URL, 
    YOUTUBE_MONGO_DB_NAME, YOUTUBE_MONGO_URL
)


class MongoDB:
    
    def __init__(self, domain='naver') -> None:
        self.client = None
        self.engine = None
        self.mongo_db_name = NAVER_MONGO_DB_NAME if domain == 'naver' else YOUTUBE_MONGO_DB_NAME
        self.mongo_db_url = NAVER_MONGO_URL if domain == 'naver' else YOUTUBE_MONGO_URL
    
    def connect(self):
        
        self.client = AsyncIOMotorClient(self.mongo_db_url)
        self.engine = AIOEngine(
            motor_client=self.client,
            database=self.mongo_db_name
        )
        print("connection with DB is successfully completed")
        
    def close(self):
        self.client.close()


naver_mongodb = MongoDB('naver')
youtube_mongodb = MongoDB('youtube')
