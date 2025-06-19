from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["test"],
)


@router.get("/ping")
async def ping():
    """
    Ручка для теста что сервис жив
    """
    return {"ping": "pong"}

