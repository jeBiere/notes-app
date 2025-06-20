from fastapi import FastAPI
import uvicorn
from routers.router import router as test_router
from routers.user_router import router as user_router
from routers.auth_router import router as auth_router
from src.config.settings import settings

app = FastAPI(title="Notes App API")

app.include_router(test_router)
app.include_router(user_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload
    )