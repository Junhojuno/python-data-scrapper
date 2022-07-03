"""app 폴더의 코드를 실행시켜주는 모듈"""
import uvicorn


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='localhost', port=8080, reload=True)
