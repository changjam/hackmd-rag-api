import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from router.router_v1 import router
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

app = FastAPI(
    docs_url=None if os.getcwd() == '/app' else '/docs',
    redoc_url=None if os.getcwd() == '/app' else '/redoc'
)

# 設定 CORS 標頭
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許的前端網域
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法
    allow_headers=["*"],  # 允許的 HTTP 標頭
)
app.include_router(router)

if __name__ == "__main__":
    port = os.environ.get('PORT', 8000)
    uvicorn.run(app, host='127.0.0.1', workers=1, port=port)