from fastapi import FastAPI
import uvicorn
from routers.router import router as test_router
from routers.user_router import router as user_router
from routers.auth_router import router as auth_router

app = FastAPI(title="Notes App API")

app.include_router(test_router)
app.include_router(user_router)
app.include_router(auth_router)

if __name__ == "__main__": 
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)