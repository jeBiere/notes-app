from fastapi import FastAPI
import uvicorn
from routers.router import router

app = FastAPI(title="Notes App API")

app.include_router(router)

if __name__ == "__main__": 
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)