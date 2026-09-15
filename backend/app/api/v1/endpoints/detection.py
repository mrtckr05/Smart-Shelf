from fastapi import APIRouter

router = APIRouter()

@router.post("/detect")
async def detect():
    return {"message: detection endpoint worked..."}

