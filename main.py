from fastapi import FastAPI
from src import tinyimg

app = FastAPI(
    title="语铄内部开发辅助工具接口",
    description="仅限语铄内部使用",
    version="0.0.1"
)

app.include_router(tinyimg.router, prefix="/tinyimg", tags=["图像优化"])

