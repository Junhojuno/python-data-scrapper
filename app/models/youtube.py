from odmantic import Model


class YoutubeModel(Model):
    """DB에 정보를 저장하기 위한 Document 모델"""
    keyword: str
    link: str
    
    class Config:
        collection = 'youtube'
