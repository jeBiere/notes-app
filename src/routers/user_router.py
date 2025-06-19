from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/registration")
async def registration():
    pass
    

