import LLM_importDS_01 as ds
from typing import Union
# 创建 FastAPI 实例
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    
    return {"message": "Hello World"}
@app.put("/user")
async def update_user(text):
    result=ds.api(text)
    return result
