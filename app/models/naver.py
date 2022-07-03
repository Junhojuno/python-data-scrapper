"""Naver image model"""
from odmantic import Model


class NaverImageModel(Model):
    keyword: str
    link: str
    height: int
    width: int
    thumbnail: str
    title: str 
    
    class Config:
        collection = 'images'
