from email.mime import image
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import naver_mongodb, youtube_mongodb
# from app.models.youtube import YoutubeModel
from app.models.naver import NaverImageModel
from app.scrapper import NaverImageScrapper


BASE_DIR = Path(__file__).resolve().parent  # app/


app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")
mongodb = naver_mongodb


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, 'title': 'Web Data Crawling Engine'}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    # 1. query에서 검색어 추출
    keyword = q
    if not keyword:
        context = {'request': request, 'title': 'Web Data Crawling Engine'}
        return templates.TemplateResponse(
            'index.html',
            context
        )
    if await mongodb.engine.find_one(NaverImageModel, NaverImageModel.keyword == keyword):
        images_info = await mongodb.engine.find(NaverImageModel, NaverImageModel.keyword == keyword)
        return templates.TemplateResponse(
            "index.html", {'request': request,
                           'title': 'Web Data Crawling Engine',
                           'images': images_info}
        )
    # 2. 검색어를 바탕으로 데이터 수집
    image_scrapper = NaverImageScrapper()
    images_info = await image_scrapper.search(keyword, 20, 10)
    
    # 3. 수집된 데이터를 DB에 저장
    image_models = []
    for image_info in images_info:
        image_model = NaverImageModel(
            keyword=keyword,
            link=image_info['link'],
            height=image_info['sizeheight'],
            width=image_info['sizewidth'],
            thumbnail=image_info['thumbnail'],
            title=image_info['title']
        )
        image_models.append(image_model)
    await mongodb.engine.save_all(image_models)  # asyncio.gather가 자체 적용된 save_all 함수
    
    return templates.TemplateResponse(
        "index.html", {'request': request,
                       'title': 'Web Data Crawling Engine',
                       'images': images_info}
    )


@app.on_event("startup")
def on_app_start():
    """before app start"""
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    """after app shutdown"""
    mongodb.close()
