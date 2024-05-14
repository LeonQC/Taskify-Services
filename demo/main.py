from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/fastapi")
async def read_root():
    return {"message": "Hello from FastAPI!"}

import os
from django.conf import settings

# 设置 DJANGO_SETTINGS_MODULE 环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

# 加载 Django 的设置
settings.configure()


from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from uvicorn import run

# Django WSGI 应用程序
django_application = get_wsgi_application()

# FastAPI 应用程序
fastapi_app = FastAPI()

@fastapi_app.get("/fastapi")
async def read_root():
    return {"message": "Hello from FastAPI!"}

# 启动两个应用程序
if __name__ == "__main__":
    run(app="main:fastapi_app", host="127.0.0.1", port=8000, log_level="info")
